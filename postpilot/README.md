# PostPilot

Facebook Page publishing scheduler with a 9-destination workflow.

## What this version does
- Connects to Facebook through the official OAuth flow (server-side token exchange).
- Lets you select a Facebook Page you manage.
- Creates/schedules Page posts through the Graph API after authorization.
- Provides 9 configurable group slots for destinations that your Meta app/account is explicitly authorized to publish to.
- Uses a minimum 5-minute interval in the scheduler.
- Keeps secrets server-side in environment variables.

## Important Meta limitation
The app does **not** bypass Facebook permissions or automate arbitrary group posting. Facebook must expose the destination through the permissions/API available to your app and account. If a group is not eligible/authorized, PostPilot marks it unavailable instead of trying to bypass the restriction.

## Local setup
1. Install Node.js 20+.
2. `npm install`
3. Copy `.env.example` to `.env` and add your Meta App ID, App Secret, and OAuth redirect URL.
4. Configure the same redirect URL and required permissions in your Meta developer app.
5. `npm start`
6. Open `http://localhost:3000`.

## GitHub Pages
The UI can be hosted on GitHub Pages, but OAuth token exchange and scheduled publishing should run on a server. Never put `META_APP_SECRET` in frontend JavaScript.
