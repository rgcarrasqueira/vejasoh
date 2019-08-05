from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Stream(models.Model):
	
	name = models.CharField(max_length=30, verbose_name=_(u'Nome da Revista'))
	url = models.URLField(max_length=200, verbose_name=_(u'Endereço da Revista'))
	date_created = models.DateField(auto_now_add=True, verbose_name=_(u'Criado em'))
	last_updated = models.DateField(auto_now=True, verbose_name=_(u'Última atualização em'))

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _(u'Stream Feed')
		verbose_name_plural = _(u'Stream Feeds')