# AWS Infrastructure & Deployment Guide — CitizenAssist AI

> **Region:** `ap-south-1` (Asia Pacific - Mumbai)  
> **Tag:** `Project=citizenassist`  
> **Target Architecture:** Single-instance containerized deployment managed via AWS Systems Manager (SSM) with zero open inbound SSH ports.

---

## 1. Inventory of AWS Resources Created

All resources below were created specifically for this deployment and tagged with `Project=citizenassist`:

| Resource Type | Resource Name / ID | Configuration / Details | Monthly Cost (Est.) |
| :--- | :--- | :--- | :--- |
| **EC2 Instance** | `i-01a644fae6eefcb3f` (`citizenassist-server`) | `t3.small` (x86_64, 2 vCPU, 2 GB RAM), Amazon Linux 2023 (`ami-0f19324397f53458f`), IMDSv2 Required | ~$15.18 |
| **EBS Root Volume** | `vol-04146aa27ca2774db` (`citizenassist-volume`) | 20 GB `gp3`, Encrypted with default KMS key | ~$1.60 |
| **Elastic IP** | `eipalloc-09b482c75046d1bd6` (`13.203.181.152`) | Attached to `i-0906416126aee904e` ($0.005/hr IPv4) | ~$3.65 |
| **Security Group** | `sg-0b30cea46a352dc6b` (`citizenassist-sg`) | Inbound HTTP port 80 open for web traffic; **Zero SSH (Port 22 closed)** | $0.00 |
| **S3 Deploy Bucket** | `citizenassist-deploy-287872994029-ap-south-1` | Private, AES256 encrypted, all public access blocked | < $0.05 |
| **IAM Role & Profile**| `citizenassist-ec2-ssm-role` / `citizenassist-ec2-instance-profile` | `AmazonSSMManagedInstanceCore` + scoped `/citizenassist/*` parameter read access | $0.00 |
| **SSM Parameter Store**| `/citizenassist/*` (9 parameters) | `SECRET_KEY`, `GEMINI_API_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, etc. | $0.00 |
| **AWS Budget** | `citizenassist-monthly-budget` | \$21.00/mo cap with email alerts at 50% and 100% to `haseebalikhan785@gmail.com` | $0.00 |
| **Total Estimated Cost** | — | — | **~$20.43 / month** |

---

## 2. HTTPS Security & Live Production Endpoints

The website is fully secured with **HTTPS (TLSv1.3)** using containerized reverse proxy with automatic Let's Encrypt certificates:
- **Live Secure Website:** **[https://13-203-181-152.sslip.io](https://13-203-181-152.sslip.io)**
- **HTTP Auto-Redirect:** Any plain HTTP access to `http://13.203.181.152` returns an automatic `301 Moved Permanently` redirect to the secure HTTPS endpoint.
- **Health Check Endpoint:** `https://13-203-181-152.sslip.io/api/health`
- **Cookie Security:** Configured with `COOKIE_SECURE=true` (`SameSite=lax; HttpOnly; Secure`) protecting citizen and administrator session tokens.
- **Port 443 Inbound:** Enabled on Security Group `sg-0b30cea46a352dc6b`, tagged with `Project=citizenassist`.

---

## 3. How to View Live Server & Application Logs

Because inbound SSH is disabled for security, manage the server using AWS Systems Manager:

### View Docker Container Logs
```bash
aws ssm send-command \
  --instance-ids i-01a644fae6eefcb3f \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["docker logs --tail 100 citizenassist"]' \
  --region ap-south-1
```

### Start an Interactive Session (Session Manager Shell)
```bash
aws ssm start-session --target i-01a644fae6eefcb3f --region ap-south-1
```

---

## 4. How to Redeploy Updates

Whenever code changes are made to the codebase:

```bash
./scripts/aws_deploy.sh
```

This single command will:
1. Bundle your local git repository (`git archive`).
2. Upload the archive to your private encrypted S3 bucket.
3. Instruct EC2 via Systems Manager to pull the archive, rebuild the multi-stage Docker image, and restart the container with zero manual SSH.

---

## 5. How to Tear Down Resources (To Stop AWS Billing)

After your hackathon judging is finished, run:

```bash
./scripts/aws_teardown.sh
```

Type `yes` when prompted. This deletes only resources tagged `Project=citizenassist`, releasing the Elastic IP and terminating the instance so no ongoing charges occur.
