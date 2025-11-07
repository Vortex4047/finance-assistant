# Vercel Deployment Guide

## 🚀 Deploy Finance Mentor AI to Vercel

### Prerequisites
- GitHub account with your repository
- Vercel account (free tier available at https://vercel.com)

### Quick Deploy (Recommended)

1. **Click the Deploy Button** (after setup):
   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Vortex4047/finance-assistant)

### Manual Deployment Steps

#### Step 1: Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

#### Step 2: Login to Vercel
```bash
vercel login
```

#### Step 3: Deploy from Command Line
```bash
# From your project directory
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? finance-assistant
# - Directory? ./
# - Override settings? No
```

#### Step 4: Set Environment Variables

After deployment, add these environment variables in Vercel Dashboard:

**Required:**
```
SECRET_KEY=your-strong-secret-key-here-min-32-chars
```

**Optional (for production features):**
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret
PLAID_ENV=production
```

**To add environment variables:**
1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable

#### Step 5: Redeploy
```bash
vercel --prod
```

### Alternative: Deploy via Vercel Dashboard

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/new

2. **Import Git Repository**
   - Click "Import Project"
   - Select "Import Git Repository"
   - Paste: `https://github.com/Vortex4047/finance-assistant`
   - Click "Import"

3. **Configure Project**
   - Project Name: `finance-assistant`
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add `SECRET_KEY` with a strong random value
   - Add other variables as needed

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment

6. **Access Your App**
   - Your app will be available at: `https://finance-assistant-xxx.vercel.app`

## ⚠️ Important Notes for Vercel Deployment

### Database Limitations
- **SQLite on Vercel**: Data is stored in `/tmp` and will be lost on each deployment
- **Recommended**: Use a managed PostgreSQL database:
  - [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres) (Recommended)
  - [Supabase](https://supabase.com) (Free tier available)
  - [Neon](https://neon.tech) (Free tier available)
  - [Railway](https://railway.app) (Free tier available)

### Setting up Vercel Postgres (Recommended)

1. In Vercel Dashboard, go to Storage tab
2. Click "Create Database"
3. Select "Postgres"
4. Choose a name and region
5. Click "Create"
6. Copy the `DATABASE_URL` connection string
7. Add it to your Environment Variables

### Session Management
- Flask sessions work but are stateless on Vercel
- For production, consider using Redis for session storage

### File Uploads
- Vercel has a 4.5MB request body limit
- For file uploads, use external storage (S3, Cloudinary, etc.)

### Cold Starts
- First request after inactivity may be slow (2-5 seconds)
- Subsequent requests are fast

## 🔧 Troubleshooting

### Issue: "Module not found" error
**Solution:** Make sure `requirements.txt` is in the root directory

### Issue: Database connection errors
**Solution:** 
- Check `DATABASE_URL` environment variable
- Ensure database is accessible from Vercel's IP ranges
- Use connection pooling

### Issue: 500 Internal Server Error
**Solution:**
- Check Vercel logs: `vercel logs`
- Or view in Dashboard → Deployments → [Your Deployment] → Logs

### Issue: Static files not loading
**Solution:**
- Ensure static files are in `static/` directory
- Check file paths are relative

## 📊 Monitoring

View your deployment logs:
```bash
vercel logs
```

Or in the Vercel Dashboard:
- Go to your project
- Click on "Deployments"
- Select a deployment
- View "Runtime Logs"

## 🔄 Continuous Deployment

Vercel automatically deploys when you push to GitHub:
- Push to `main` branch → Production deployment
- Push to other branches → Preview deployment

## 🌐 Custom Domain

1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. Wait for SSL certificate (automatic)

## 💰 Pricing

- **Hobby (Free)**: Perfect for personal projects
  - 100 GB bandwidth/month
  - Unlimited deployments
  - Automatic HTTPS

- **Pro ($20/month)**: For production apps
  - 1 TB bandwidth/month
  - Advanced analytics
  - Team collaboration

## 📚 Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask on Vercel Guide](https://vercel.com/guides/using-flask-with-vercel)
- [Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

## 🎉 Success!

Once deployed, your Finance Mentor AI will be live at:
`https://your-project-name.vercel.app`

Share it with the world! 🚀
