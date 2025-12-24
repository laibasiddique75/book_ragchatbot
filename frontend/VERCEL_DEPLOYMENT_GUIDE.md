# Deploying Frontend to Vercel

## Prerequisites
- A Vercel account (sign up at https://vercel.com)
- Your frontend code ready for deployment
- Your backend deployed and running (with a public URL)

## Steps to Deploy

### 1. Prepare Your Repository
- Push your frontend code to a Git repository (GitHub, GitLab, or Bitbucket)
- Make sure all necessary files are included:
  - package.json
  - docusaurus.config.js
  - src/ folder with components
  - vercel.json (configuration file)
  - .env.example (for reference)

### 2. Deploy to Vercel
1. Go to https://vercel.com and log in to your account
2. Click "New Project" or "Deploy"
3. Import your Git repository
4. Vercel will automatically detect that this is a Docusaurus project
5. In the build settings:
   - Build Command: `npm run build` (or `yarn build`)
   - Output Directory: `build`
   - Root Directory: `.` (current directory)

### 3. Set Environment Variables
In your Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following environment variable:
   - Key: `REACT_APP_BACKEND_URL`
   - Value: Your deployed backend URL (e.g., `https://your-backend-name.onrender.com`)

### 4. Deploy
- Click "Deploy" and Vercel will build and deploy your application
- Monitor the build logs to ensure everything works correctly

## Important Notes

1. **Backend URL**: Make sure your backend is deployed and accessible via HTTPS before setting the `REACT_APP_BACKEND_URL` variable.

2. **Build Process**: Docusaurus will build the static site during deployment. The build command is specified in your package.json.

3. **Custom Domain**: You can add a custom domain in the Vercel dashboard after deployment.

4. **Environment Variables**: The `REACT_APP_BACKEND_URL` environment variable will be available to your frontend at build time and runtime.

5. **API Communication**: The chat functionality will use the backend URL you specify in the environment variable.

## Troubleshooting

- If the chat is not working, check that the backend URL is correctly set in environment variables
- Verify that your backend is deployed and accessible
- Check browser console for any CORS or network errors
- Make sure your backend allows requests from your frontend domain

## Updating Your Deployment

After making changes to your code:
1. Commit and push changes to your Git repository
2. Vercel will automatically deploy the new version
3. Monitor the deployment logs for any issues

## Example
Once deployed, your site will be accessible at:
- `https://your-project-name.vercel.app`

The chat functionality will connect to your backend at the URL you specified in the environment variables.