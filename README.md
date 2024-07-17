# AWS 3-Tier App Architecture
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
- Stress test the dummy application to show that the architecture is functional. We should see increased CPU utilization across all of our instances,
- ~~Add data subnets which are private subnets that are used to host application Databases~~.

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
  -  ~~CloudWatch Alarms~~.

### Step 3.0
When integrating the load balancer, we had to specify at least two public subnets created by the networking stack. We did not want to list them manually because the template 
would start looking like C++ libraries before variadic templates. In the end, we wrote a CloudFormation 
[macro](https://github.com/MogomotsiFM/aws-3-tier-app-architecture/blob/main/generate_sequence_macro.yaml) 
that takes a range of numbers and a template snippet and maps it into an array of snippets. 

### Step 3.1
We have now integrated every target resource but the autoscaling policy and alarms. We installed the httpd server using EC2 instance user data. The server replies with the hostname of 
an EC2 instance. This allowed us to show that the network is fully functional and the load balancer distributes the requests between the instances. The following is the resource map from the load balancer console:
![Screenshot 2024-07-14 032429](https://github.com/user-attachments/assets/09455a3b-50f7-47af-8575-22c620c1c03b)

### Step 3.2
We have integrated the average CPU utilization target tracking AutoScaling policy. This policy automatically creates CloudWatch alarms for us. Using the EC2 Instance user-data script, we have installed and started a 
tool to stress the CPU of an instance. This shows that the number of instances scales in response to the average CPU utilization. The following figure shows autoscaling in action:
![Screenshot 2024-07-16 142009](https://github.com/user-attachments/assets/662deaab-a5cd-4e4f-9c6c-44c16a6075b2)

## Step 4
At this point, we want to test the architecture from the internet. As seen in the ***golden_ami.sh*** script, we created the "golden AMI" by:
- Launching an EC2 instance with an Amazon Linux 2 AMI,
- Installing Python and Pip,
- Installing FastAPI and Gunicorn,
- Copying our dummy application into the EC2 instance,
- Then creating a custom AMI from this instance.

Then we tested the API using Postman. Postman makes it easy to specify the number of requests and the delay between them. You could also set the number of 
virtual users and model numerous traffic patterns. The following figure shows the average CPU utilization per EC2 instance.
![Screenshot 2024-07-17 154732](https://github.com/user-attachments/assets/ec5a583f-c871-46e7-8791-8a81feb859d3)

The following figures show the corresponding metrics for the target group. 
![Screenshot 2024-07-17 160602](https://github.com/user-attachments/assets/dc311c57-67fa-433d-a859-b7b589544c2e)

 ## Possible Improvements
 - Re-use the generate-sequence macro in the network resources template,
 - The number of EC2 instances in the Auto Scaling Group is a bit noisy, as seen in the target group metrics. This could be solved by specifying a "cooldown" period
   for the auto-scaling policy. We could also use two simple scaling policies instead of the target tracking policy. This would allow us to specify when to scale in the fleet,
- Allocating a much smaller public subnet compared to the private one,
- Make the creation of public subnets optional which is ideal for worker environments,
- Create the EC2 instance profile and associate its role with the **AmazonSSMManagedInstanceCore** managed policy. This is required if we ever need to SSH
  into one of the servers without open port 22. 

## Conclusion
We used AWS CloudFormation to provision all the resources required for a three-tier architecture. We also "deployed" a dummy application on our servers using a custom AMI. 
The architecture was tested using Postman making it effortless to define virtual users and traffic patterns. The test traffic showed that the network foundation is 
functional and that the number of EC2 instances scales in response to the number of requests. We have also proposed various improvements to the architecture.
