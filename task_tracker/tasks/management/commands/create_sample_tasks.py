from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task, Subtask
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates sample tasks and subtasks'

    def handle(self, *args, **kwargs):
        # Tasks with their specific subtasks
        tasks_data = [
            {
                "name": "تجميع وتحليل البيانات",
                "minutes_to_deadline": 10,
                "subtasks": [
                    "جمع البيانات من المصادر",
                    "تنظيف وتنسيق البيانات",
                    "تحليل الاتجاهات الرئيسية",
                    "إعداد الرسوم البيانية",
                    "كتابة التقرير النهائي"
                ]
            },
            {
                "name": "تطوير واجهة المستخدم",
                "minutes_to_deadline": 20,
                "subtasks": [
                    "تصميم الواجهة الرئيسية",
                    "برمجة العناصر التفاعلية",
                    "تنفيذ التصميم المتجاوب",
                    "اختبار التوافق مع المتصفحات",
                    "تحسين سرعة التحميل"
                ]
            },
            {
                "name": "اختبار النظام",
                "minutes_to_deadline": 30,
                "subtasks": [
                    "إعداد بيئة الاختبار",
                    "اختبار الوظائف الأساسية",
                    "اختبار الأداء والتحمل",
                    "توثيق الأخطاء والمشاكل",
                    "التحقق من إصلاح الأخطاء"
                ]
            },
            {
                "name": "كتابة الوثائق",
                "minutes_to_deadline": 40,
                "subtasks": [
                    "إعداد دليل المستخدم",
                    "توثيق واجهة برمجة التطبيقات",
                    "كتابة الوثائق التقنية",
                    "إعداد أمثلة الاستخدام",
                    "مراجعة وتحديث الوثائق"
                ]
            },
            {
                "name": "تحسين الأداء",
                "minutes_to_deadline": 50,
                "subtasks": [
                    "تحليل نقاط الضعف",
                    "تحسين استعلامات قاعدة البيانات",
                    "تحسين تحميل الصفحات",
                    "تقليل استهلاك الموارد",
                    "قياس التحسينات وتوثيقها"
                ]
            },
            {
                "name": "تطوير واجهة برمجة التطبيقات",
                "minutes_to_deadline": 60,
                "subtasks": [
                    "تصميم هيكل API",
                    "تنفيذ نقاط النهاية",
                    "إضافة المصادقة والتفويض",
                    "توثيق النقاط النهائية",
                    "اختبار وتحسين الأداء"
                ]
            },
            {
                "name": "إدارة قاعدة البيانات",
                "minutes_to_deadline": 70,
                "subtasks": [
                    "تصميم المخطط الهيكلي",
                    "تنفيذ النماذج والعلاقات",
                    "إعداد النسخ الاحتياطي",
                    "تحسين أداء الاستعلامات",
                    "إدارة الترحيل والتحديثات"
                ]
            },
            {
                "name": "تحسين تجربة المستخدم",
                "minutes_to_deadline": 80,
                "subtasks": [
                    "تحليل سلوك المستخدم",
                    "تحسين التنقل والتفاعل",
                    "تحسين الوصول والاستخدام",
                    "إجراء اختبارات المستخدم",
                    "تنفيذ التحسينات المقترحة"
                ]
            },
            {
                "name": "تطوير الخدمات الخلفية",
                "minutes_to_deadline": 90,
                "subtasks": [
                    "تصميم هيكل الخدمات",
                    "تنفيذ المعالجة الأساسية",
                    "إضافة التوثيق والسجلات",
                    "تنفيذ المصادقة والأمان",
                    "اختبار وتحسين الأداء"
                ]
            },
            {
                "name": "اختبار الأمان",
                "minutes_to_deadline": 100,
                "subtasks": [
                    "تحليل نقاط الضعف الأمنية",
                    "اختبار الاختراق",
                    "مراجعة التشفير والحماية",
                    "اختبار المصادقة والتفويض",
                    "توثيق وإصلاح الثغرات"
                ]
            },
            {
                "name": "نشر التطبيق",
                "minutes_to_deadline": 110,
                "subtasks": [
                    "إعداد بيئة الإنتاج",
                    "نشر قاعدة البيانات",
                    "نشر التطبيق والخدمات",
                    "اختبار النشر والتشغيل",
                    "مراقبة الأداء والاستقرار"
                ]
            }
        ]

        # Create tasks and their subtasks
        for task_data in tasks_data:
            # Calculate deadline using minutes
            deadline = timezone.now() + timedelta(minutes=task_data["minutes_to_deadline"])
            
            task = Task.objects.create(
                name=task_data["name"],
                deadline=deadline
            )
            
            # Create specific subtasks for this task
            for subtask_name in task_data["subtasks"]:
                Subtask.objects.create(
                    task=task,
                    name=subtask_name,
                    assignee=None
                )

        self.stdout.write(self.style.SUCCESS('Successfully created sample tasks and subtasks'))

        # Print helpful information about deadlines
        self.stdout.write("\nTask Deadlines:")
        for task in Task.objects.all().order_by('deadline'):
            time_remaining = task.deadline - timezone.now()
            minutes_remaining = int(time_remaining.total_seconds() / 60)
            self.stdout.write(f"- {task.name}: {minutes_remaining} minutes remaining")

"""
Common datetime formats in Django:

1. Creating datetime objects:
   from django.utils import timezone
   from datetime import datetime, timedelta
   
   # Current time
   now = timezone.now()
   
   # Specific time
   specific_time = timezone.make_aware(datetime(2024, 1, 20, 15, 30))
   
   # Adding time
   ten_minutes_later = now + timedelta(minutes=10)
   one_hour_later = now + timedelta(hours=1)

2. Template formatting:
   {{ task.deadline|date:"Y-m-d H:i" }}  # 2024-01-20 15:30
   {{ task.deadline|date:"F j, Y, g:i a" }}  # January 20, 2024, 3:30 p.m.
   {{ task.deadline|time:"H:i" }}  # 15:30

3. Time calculations:
   time_remaining = task.deadline - timezone.now()
   minutes_remaining = time_remaining.total_seconds() / 60

4. Common timedelta uses:
   timedelta(days=1)  # 1 day
   timedelta(hours=2)  # 2 hours
   timedelta(minutes=30)  # 30 minutes
   timedelta(seconds=45)  # 45 seconds
   
5. Timezone awareness:
   # Always use timezone.now() instead of datetime.now()
   # Always make datetime objects timezone-aware using timezone.make_aware()
   # Use settings.TIME_ZONE to specify your application's timezone
""" 