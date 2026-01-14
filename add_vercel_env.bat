@echo off
echo Adding environment variables to Vercel...
echo.

cd clara-onboarding-website

echo Adding RETELL_API_TOKEN...
vercel env add RETELL_API_TOKEN production
echo key_f179b569899f2ab68c5f875033e0

echo.
echo Adding DB_HOST...
vercel env add DB_HOST production
echo db.hpslbymjobdvjmrgfweo.supabase.co

echo.
echo Adding DB_PORT...
vercel env add DB_PORT production
echo 5432

echo.
echo Adding DB_NAME...
vercel env add DB_NAME production
echo postgres

echo.
echo Adding DB_USER...
vercel env add DB_USER production
echo postgres

echo.
echo Adding DB_PASSWORD...
vercel env add DB_PASSWORD production
echo y7569811281y

echo.
echo Done! Environment variables added.
echo Now redeploy with: vercel --prod
pause
