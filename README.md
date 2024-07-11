# AWS 3-tier app architecture
The plan is to create all the resources required for a three-tier architecture using AWS CloudFormation. This includes a VPC, public and private subnets, 
an Internet Gateway, security groups, application load balancer, and routing tables.
## Plan
- Create an architecture with one public and one private subnet,
- Make it highly available by creating public and private subnets in multiple availability zones,
- Integrate an auto-scaling group and, by extension, launch EC2 instances in the subnets,
- Use the EC2 Instance user data to launch a dummy application,
- Stress test the dummy application to show that the architecture is functional.

## Step 1
![Screenshot 2024-07-12 000740](https://github.com/user-attachments/assets/6df62c8e-872c-42d9-92de-979e520e962b)
