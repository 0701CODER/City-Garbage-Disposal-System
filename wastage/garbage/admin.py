from django.contrib import admin
from .models import Collection, Claim, NGOExtra, DisposalExtra, Notice
# Register your models here. (by sumit.luv)
class NGOExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(NGOExtra, NGOExtraAdmin)

class DisposalExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(DisposalExtra, DisposalExtraAdmin)

class CollectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Collection, CollectionAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)

class ClaimAdmin(admin.ModelAdmin):
    pass
admin.site.register(Claim, ClaimAdmin)
