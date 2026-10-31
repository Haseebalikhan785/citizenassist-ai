#!/bin/bash
# ==============================================================================
# CitizenAssist AI - AWS Redeploy Script
# Bundles current repository, uploads to S3, and triggers remote rebuild via SSM.
# ==============================================================================

set -e

REGION="ap-south-1"
BUCKET="citizenassist-deploy-287872994029-ap-south-1"
INSTANCE_ID="i-0906416126aee904e"
PUBLIC_IP="13.203.181.152"

echo "============================================================"
echo "  CitizenAssist AI - Redeploying to AWS EC2 ($REGION)..."
echo "============================================================"

# 1. Verify AWS CLI
if ! command -v aws &> /dev/null; then
    echo "ERROR: AWS CLI is not installed or not in PATH."
    exit 1
fi

# 2. Check Identity
echo "[1/4] Verifying AWS credentials..."
if ! aws sts get-caller-identity --region "$REGION" > /dev/null 2>&1; then
    echo "Session expired or not logged in. Launching 'aws login'..."
    aws login
fi

# 3. Create deploy archive
echo "[2/4] Creating deployment archive from git..."
git archive --format=tar.gz -o deploy_bundle.tar.gz HEAD

# 4. Upload to S3
echo "[3/4] Uploading bundle to S3 ($BUCKET)..."
aws s3 cp deploy_bundle.tar.gz "s3://$BUCKET/deploy_bundle.tar.gz" --region "$REGION"
rm deploy_bundle.tar.gz

# 5. Trigger Remote Build & Restart via AWS Systems Manager
echo "[4/4] Triggering build and container restart via SSM..."
COMMAND_ID=$(aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunShellScript" \
  --comment "Redeploy CitizenAssist AI container" \
  --parameters 'commands=[
    "set -e",
    "mkdir -p /opt/citizenassist/src /var/lib/citizenassist/data",
    "aws s3 cp s3://'"$BUCKET"'/deploy_bundle.tar.gz /opt/citizenassist/deploy_bundle.tar.gz --region '"$REGION"'",
    "tar -xzf /opt/citizenassist/deploy_bundle.tar.gz -C /opt/citizenassist/src",
    "> /etc/citizenassist.env",
    "aws ssm get-parameters-by-path --path /citizenassist/ --with-decryption --region '"$REGION"' --query \"Parameters[*].[Name,Value]\" --output text | while read -r name val; do varname=$(basename \"$name\"); if [[ \"$val\" == \"placeholder_until_user_entry\" ]]; then echo \"$varname=\" >> /etc/citizenassist.env; else echo \"$varname=$val\" >> /etc/citizenassist.env; fi; done",
    "echo \"DATABASE_URL=sqlite:////app/data/citizenassist.db\" >> /etc/citizenassist.env",
    "chmod 600 /etc/citizenassist.env",
    "cd /opt/citizenassist/src",
    "docker build -t citizenassist:latest .",
    "docker stop citizenassist 2>/dev/null || true",
    "docker rm citizenassist 2>/dev/null || true",
    "docker run -d --name citizenassist --restart unless-stopped -p 80:8000 --env-file /etc/citizenassist.env -v /var/lib/citizenassist/data:/app/data citizenassist:latest",
    "sleep 6",
    "curl -s http://127.0.0.1/api/health"
  ]' \
  --region "$REGION" \
  --query "Command.CommandId" \
  --output text)

echo "SSM Deployment Command sent: $COMMAND_ID"
echo "Waiting for build and container launch to complete..."

while true; do
    STATUS=$(aws ssm get-command-invocation \
      --command-id "$COMMAND_ID" \
      --instance-id "$INSTANCE_ID" \
      --region "$REGION" \
      --query "Status" \
      --output text 2>/dev/null || echo "Pending")
    
    if [ "$STATUS" == "Success" ]; then
        echo "============================================================"
        echo "  DEPLOYMENT SUCCESSFUL!"
        echo "  Live Website: http://$PUBLIC_IP"
        echo "============================================================"
        break
    elif [ "$STATUS" == "Failed" ] || [ "$STATUS" == "Cancelled" ]; then
        echo "ERROR: Remote deployment $STATUS."
        aws ssm get-command-invocation \
          --command-id "$COMMAND_ID" \
          --instance-id "$INSTANCE_ID" \
          --region "$REGION" \
          --query "StandardErrorContent" \
          --output text
        exit 1
    fi
    sleep 5
done
