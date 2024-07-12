# AWS 3-tier app architecture
The plan is to create all the resources required for a three-tier architecture using AWS CloudFormation. This includes a VPC, public and private subnets, 
an Internet Gateway, security groups, application load balancer, and routing tables.
## Plan
- Create an architecture with one public and one private subnet,
  - Add a NAT Gateway so that Instances in a private subnet can download the dummy application,
- Make it highly available by creating public and private subnets in multiple availability zones,
- Integrate an auto-scaling group and, by extension, launch EC2 instances in the subnets,
- Use the EC2 Instance user data to launch a dummy application,
- Stress test the dummy application to show that the architecture is functional.

## Step 1
![Screenshot 2024-07-12 000740](https://github.com/user-attachments/assets/6df62c8e-872c-42d9-92de-979e520e962b)
## Step 1.1
![Screenshot 2024-07-12 020412](https://github.com/user-attachments/assets/9a9c8136-e8b2-4b2d-8177-7c196a961c1a)
In this step, we added a NAT Gateway to our architecture. Given this configuration, we can perform the following actions in order:
- Launch an instance in the private subnet,
- Associate it with an Instance profile role,
- Attach the AmazonSSMManagedInstanceCore managed policy to the role,
- Use SSM Session Manager to tunnel into the instance,
- Ping, for example, www.google.com.
