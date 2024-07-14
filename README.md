# AWS 3-tier app architecture
The plan is to create all the resources required for a three-tier architecture using AWS CloudFormation. This includes a VPC, public and private subnets, 
an Internet Gateway, security groups, application load balancer, and routing tables.
## Plan
- Create an architecture with one public and one private subnet,
  - Add a NAT Gateway so that Instances in a private subnet can download the dummy application,
- Make it highly available by creating public and private subnets in multiple availability zones,
  -  Show that when all the resources are in one availability zone (AZ), then the architecture resembles the ones in Step 1,
  -  Create resources in multiple AZs,
- Intermission,
- Integrate an auto-scaling group and, by extension, launch EC2 instances in the subnets,
  - Use the EC2 Instance user data to launch a dummy application,
- Add data subnets which are private subnets that are used to host application Databases,
- Stress test the dummy application to show that the architecture is functional. We should see increased CPU utilization across all of our instances.

## Step 1
![Screenshot 2024-07-12 000740](https://github.com/user-attachments/assets/6df62c8e-872c-42d9-92de-979e520e962b)
## Step 1.1
![Screenshot 2024-07-12 020412](https://github.com/user-attachments/assets/9a9c8136-e8b2-4b2d-8177-7c196a961c1a)
In this step, we added a NAT Gateway to our architecture. Given this configuration, we can perform the following actions in the given order:
- Launch an instance in the private subnet,
- Associate it with an Instance profile role,
- Attach the AmazonSSMManagedInstanceCore managed policy to the role,
- Use SSM Session Manager to tunnel into the instance,
- Ping, for example, www.google.com.

## Step 2.1
We have updated the template for deploying high-availability infrastructure. We want to show that the architecture is the same as we already had when all resources are deployed to one AZ.

![dev_setup_architecture](https://github.com/user-attachments/assets/d5ce94de-d051-4baa-a27d-116ccb79c84d)
We performed the following actions in  the given order to test this new network:
- Launch two instances with the associated key pair, one per subnet,
- Modify the security groups created by CloudFormation to allow SSH access on port 22,
  -  This is not required for our application because we can always use SSM Session Manager if we want to access Instances,
- SSH into the EC2 instance in the public subnet,
- From that instance, SSH into the EC2 instance in the private subnet,
- Ping any website to show that the NAT Gateway was configured correctly,
- The following image shows the output when following these steps.
![dev_setup_demo](https://github.com/user-attachments/assets/7d62ff29-01e9-4f13-8da0-2663d9a4490a)

## Step 2.2
![high_availability_architecture](https://github.com/user-attachments/assets/31231009-eeef-4a95-a634-cb72aad2a6c6)

## Intermission
- Save the Cloudformation template to an S3 bucket so that it may be nested in another stack using the **AWS::CloudFormation::Stack** resource,
- YAML is easy to read but I struggled to integrate the Fn::ForEach intrinsic function largely due to space-based formatting,
- NAT Gateway is not highly available and we do not even address that,
- The public subnet address space (CIDR) is as large as that of the private subnets. This is the case even when the public subnet will likely only host the Application Load Balancers,
- Clean up tasks,
  - Export some resources so that the template is reusable,
  - Tagging all the resources we are creating,
  - Improve parameter names,
- AWS CloudFormation could do with a [range intrinsic function](https://github.com/aws-cloudformation/cfn-language-discussion/issues/144) to generate arrays given the start and end values,
- Should creating public subnets be optional? This could be desirable if we want to provision resources for a headless, worker application that reads from an SQS queue,
  - Should we also include the application or service names as an input parameter to the networking template?

## Step 3
- The idea is to create a template to provision application-specific resources. In this case, the following resources will be included:
  -  Application Load Balancer,
  -  HTTP Listener,
  -  Target Group,
  -  Launch Template,
  -  AutoScaling Group,
  -  AutoScaling Policy,
  -  CloudWatch Alarms.

### Step 3.0
When integrating the load balancer, we had to specify at least two public subnets created by the networking stack. We did not want to list them manually because the template 
would start looking like C++ libraries before variadic templates. In the end, we wrote a CloudFormation 
[macro](https://github.com/MogomotsiFM/aws-3-tier-app-architecture/blob/main/generate_sequence_macro.yaml) 
that takes a range of numbers and a template snippet and maps it into an array of snippets. 

### Step 3.1
We have now integrated every target resource but the autoscaling policy and alarms. We installed the httpd server using EC2 instance user data. The following is the resource map from the load balancer console:
![Screenshot 2024-07-14 032429](https://github.com/user-attachments/assets/09455a3b-50f7-47af-8575-22c620c1c03b)

### Step 3.2
Integrating autoscaling policy and alarms.
