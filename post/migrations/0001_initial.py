# Generated by Django 4.2.4 on 2023-08-28 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("COMMON", "COMMON"),
                            ("NEMO", "NEMO"),
                            ("ADMIN", "ADMIN"),
                        ],
                        max_length=15,
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=30, null=True)),
                ("content", models.TextField(default="")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("content", models.TextField(default="")),
                ("password", models.CharField(max_length=4)),
                (
                    "post",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="post.post",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MaintainerPost",
            fields=[],
            options={
                "verbose_name": "게시글 (관리자용)",
                "verbose_name_plural": "게시글들 (관리자용)",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("post.post",),
        ),
    ]
