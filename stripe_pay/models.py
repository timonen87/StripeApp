from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    class TypeCurrency(models.TextChoices):
        RUB = "rub", "Рубли"
        USD = "usd", "Доллары"

    name = models.CharField(max_length=100, verbose_name="Название")
    descriptiom = models.CharField(max_length=250, verbose_name="Описание")
    price = models.IntegerField(default=0, verbose_name="Цена")
    currency = models.CharField(
        max_length=5,
        choices=TypeCurrency.choices,
        default=TypeCurrency.USD,
        verbose_name="Валюта",
    )

    def __str__(self):
        return self.name

    def get_formatted_price(self):
        return "{0:.2f}".format(self.price / 100)
        # return self.price / 100

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"


class Discount(models.Model):
    class TypeDiscount(models.TextChoices):
        PERCENTAGE = "percentage", "В процентах"
        FIXED = "fixed", "Фикс"

    name = models.CharField(max_length=255, verbose_name="Скидка")
    amount = models.IntegerField(
        blank=True,
        verbose_name="Значение скидки",
    )
    type = models.CharField(
        max_length=32,
        choices=TypeDiscount.choices,
        default=TypeDiscount.PERCENTAGE,
        verbose_name="Тип скидки",
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return self.name

    @property
    def amount_formatted_price(self):
        return "{0:.2f}".format(self.amount / 100)
        # return self.amount / 100


class Tax(models.Model):
    name = models.CharField(
        max_length=255,
    )
    percent = models.IntegerField(
        default=20,
    )

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return self.name


class Order(models.Model):
    class TypeCurrency(models.TextChoices):
        RUB = "rub", "Рубли"
        USD = "usd", "Доллары"

    items = models.ManyToManyField(
        Item, verbose_name="Список элементов", related_name="items"
    )
    currency = models.CharField(
        choices=TypeCurrency.choices,
        default=TypeCurrency.USD,
        max_length=10,
        verbose_name="Валюта",
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Скидка",
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Налог",
    )

    class Meta:
        verbose_name = "Ордер"
        verbose_name_plural = "Ордер"
        default_related_name = "order"

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.price

        if self.discount is not None:
            discount = self.discount.amount
            if self.discount.type == "percentage":
                total_price = total_price * (100 - discount) / 100
            else:
                total_price = total_price - self.discount.amount

        if self.tax is not None:
            tax = self.tax.percent
            total_price += total_price * tax / 100

        return round(int(float(total_price)))

    @property
    def total_formatted_price(self):
        return "{0:.2f}".format(self.total_price / 100)
