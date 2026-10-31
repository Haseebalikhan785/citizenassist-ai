#!/bin/bash
# ==============================================================================
# CitizenAssist AI - AWS Teardown Script
# Safely tears down ONLY resources tagged with Project=citizenassist to stop charges.
# DO NOT RUN THIS UNTIL AFTER YOUR DEMO / HACKATHON EVALUATION IS FINISHED!
# ==============================================================================

set -e

REGION="ap-south-1"
ACCOUNT_ID="287872994029"
INSTANCE_ID="i-0906416126aee904e"
EIP_ALLOC="eipalloc-09b482c75046d1bd6"
SG_ID="sg-0b30cea46a352dc6b"
BUCKET="citizenassist-deploy-287872994029-ap-south-1"
ROLE_NAME="citizenassist-ec2-ssm-role"
PROFILE_NAME="citizenassist-ec2-instance-profile"
BUDGET_NAME="citizenassist-monthly-budget"

echo "============================================================"
echo "  CitizenAssist AI - AWS Infrastructure Teardown"
echo "  Region: $REGION | Account: $ACCOUNT_ID"
echo "============================================================"
echo ""
echo "WARNING: This will permanently delete the EC2 instance, Elastic IP,"
echo "S3 deployment bucket, IAM role, and SSM parameters."
echo ""
read -p "Are you sure you want to tear down all resources? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Teardown aborted."
    exit 0
fi

if ! aws sts get-caller-identity --region "$REGION" > /dev/null 2>&1; then
    echo "Session expired or not logged in. Launching 'aws login'..."
    aws login
fi

echo ""
echo "[1/8] Terminating EC2 Instance ($INSTANCE_ID)..."
aws ec2 terminate-instances --instance-ids "$INSTANCE_ID" --region "$REGION" > /dev/null 2>&1 || true
echo "Waiting for instance to terminate..."
aws ec2 wait instance-terminated --instance-ids "$INSTANCE_ID" --region "$REGION" > /dev/null 2>&1 || true
echo "✓ EC2 instance terminated."

echo "[2/8] Releasing Elastic IP ($EIP_ALLOC)..."
aws ec2 release-address --allocation-id "$EIP_ALLOC" --region "$REGION" > /dev/null 2>&1 || true
echo "✓ Elastic IP released."

echo "[3/8] Deleting Security Group ($SG_ID)..."
aws ec2 delete-security-group --group-id "$SG_ID" --region "$REGION" > /dev/null 2>&1 || true
echo "✓ Security group deleted."

echo "[4/8] Emptying and deleting S3 deployment bucket ($BUCKET)..."
aws s3 rm "s3://$BUCKET" --recursive --region "$REGION" > /dev/null 2>&1 || true
aws s3api delete-bucket --bucket "$BUCKET" --region "$REGION" > /dev/null 2>&1 || true
echo "✓ S3 bucket deleted."

echo "[5/8] Deleting SSM Parameter Store parameters (/citizenassist/*)..."
PARAMS=$(aws ssm get-parameters-by-path --path /citizenassist/ --query "Parameters[*].Name" --output text --region "$REGION" 2>/dev/null || true)
if [ -n "$PARAMS" ]; then
    aws ssm delete-parameters --names $PARAMS --region "$REGION" > /dev/null 2>&1 || true
fi
echo "✓ SSM parameters deleted."

echo "[6/8] Deleting IAM Instance Profile and Role..."
aws iam remove-role-from-instance-profile --instance-profile-name "$PROFILE_NAME" --role-name "$ROLE_NAME" > /dev/null 2>&1 || true
aws iam delete-instance-profile --instance-profile-name "$PROFILE_NAME" > /dev/null 2>&1 || true
aws iam delete-role-policy --role-name "$ROLE_NAME" --policy-name citizenassist-permissions > /dev/null 2>&1 || true
aws iam detach-role-policy --role-name "$ROLE_NAME" --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore > /dev/null 2>&1 || true
aws iam delete-role --role-name "$ROLE_NAME" > /dev/null 2>&1 || true
echo "✓ IAM role and instance profile deleted."

echo "[7/8] Deleting AWS Budget ($BUDGET_NAME)..."
aws budgets delete-budget --account-id "$ACCOUNT_ID" --budget-name "$BUDGET_NAME" > /dev/null 2>&1 || true
echo "✓ AWS budget deleted."

echo "[8/8] Logging out from AWS CLI..."
aws logout > /dev/null 2>&1 || true
echo "✓ Logged out from AWS CLI."

echo ""
echo "============================================================"
echo "  TEARDOWN COMPLETE. All CitizenAssist resources removed."
echo "============================================================"
