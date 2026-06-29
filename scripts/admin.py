from django.contrib import admin

from .models import Script, ScriptStep


class ScriptStepInline(admin.TabularInline):
    model = ScriptStep
    extra = 0


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    inlines = [ScriptStepInline]
