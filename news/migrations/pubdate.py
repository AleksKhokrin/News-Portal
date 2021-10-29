from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', 'initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pubDate',
            field=models.DateTimeField(verbose_name='дата и время публикации статьи/новости'),
        ),
    ]
