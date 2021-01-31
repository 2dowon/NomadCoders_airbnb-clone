import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(models.Model):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:  # 새로운 예약의 경우
            start = self.check_in
            end = self.check_out
            difference = end - start
            # 체크인과 체크아웃 사이에 예약이 존재하는지를 필터로 확인
            # existing_booked_day = BookedDay.objects.filter(
            #     day__range=(start, end)
            # ).exists()
            # 다른 방을 예약할 때 날짜가 겹쳤을 때 데이터베이스에 저장이 안되는 에러 해결
            filter_room = BookedDay.objects.filter(reservation__room=self.room)
            existing_booked_day = filter_room.filter(day__range=(start, end)).exists()

            if not existing_booked_day:  # 만약 해당 날짜에 예약이 없다면
                super().save(*args, **kwargs)  # 예약을 저장하고
                for i in range(difference.days + 1):  # 예약 날짜를 BookedDay로 만들기
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return

        return super().save(*args, **kwargs)
