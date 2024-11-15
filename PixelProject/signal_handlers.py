# your_app/signal_handlers.py

from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render


@receiver(pre_save, sender=Session)
def session_pre_save(sender, **kwargs):
    session = kwargs['instance']
    if hasattr(session, 'session_key'):
        user_id = Session.objects.get(session_key=session.session_key).get('_auth_user_id')
        if user_id:
            last_login = User.objects.get(id=user_id).last_login
            if last_login and timezone.now() - last_login > timezone.timedelta(minutes=300):
                # 用户最后一次活动时间超过15分钟未活动，视为掉线
                # 这里可以执行登出操作或其他逻辑
                return render(session, "login.html", locals())
