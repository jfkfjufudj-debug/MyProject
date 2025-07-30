# 🚀 دليل النشر على Railway

## الخطوة 1: إعداد GitHub Repository

### 1. إنشاء Repository جديد على GitHub:
```
1. اذهب إلى github.com
2. اضغط "New repository"
3. اسم المشروع: "video-extractor-server"
4. اجعله Public
5. اضغط "Create repository"
```

### 2. رفع الكود:
```bash
# في مجلد المشروع
git init
git add .
git commit -m "Initial commit - Video Extractor Server"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/video-extractor-server.git
git push -u origin main
```

## الخطوة 2: النشر على Railway

### 1. إنشاء مشروع جديد:
```
1. اذهب إلى railway.app
2. اضغط "New Project"
3. اختر "Deploy from GitHub repo"
4. اختر repository الذي أنشأته
```

### 2. تكوين المتغيرات:
```
في Railway Dashboard:
1. اذهب إلى "Variables" tab
2. أضف المتغيرات التالية:
   - PORT: (سيتم تعيينه تلقائياً)
   - API_KEY: your-secure-api-key-here
```

### 3. انتظار النشر:
```
- Railway سيقوم بـ:
  ✅ تحميل الكود
  ✅ تثبيت المتطلبات
  ✅ تشغيل السيرفر
  ✅ إعطاؤك رابط مجاني
```

## الخطوة 3: اختبار السيرفر المنشور

### 1. الحصول على الرابط:
```
في Railway Dashboard ستجد:
- رابط مثل: https://your-app-name.up.railway.app
```

### 2. اختبار الـ API:
```bash
# اختبار Health Check
curl https://your-app-name.up.railway.app/health

# اختبار استخراج فيديو
curl -X POST "https://your-app-name.up.railway.app/api/v1/extract" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## 🎯 البدائل الأخرى:

### Render.com:
```
1. اذهب إلى render.com
2. "New Web Service"
3. ربط GitHub repository
4. Build Command: pip install -r requirements.txt
5. Start Command: uvicorn server_final:app --host 0.0.0.0 --port $PORT
```

### Heroku:
```
1. اذهب إلى heroku.com
2. "Create new app"
3. ربط GitHub repository
4. Enable automatic deploys
```

## 🔧 نصائح مهمة:

### 1. الأمان:
- غير API_KEY من القيمة الافتراضية
- استخدم HTTPS دائماً
- لا تشارك API Key علناً

### 2. المراقبة:
- تابع logs في Railway Dashboard
- راقب استخدام الموارد
- اختبر الـ API بانتظام

### 3. التحديثات:
- أي تغيير في GitHub سيؤدي لإعادة نشر تلقائي
- اختبر التغييرات محلياً أولاً
- استخدم branches للتطوير

## 🎉 بعد النشر الناجح:

✅ السيرفر متاح 24/7
✅ SSL مجاني
✅ نشر تلقائي من GitHub
✅ مراقبة وlogs
✅ رابط مجاني دائم
