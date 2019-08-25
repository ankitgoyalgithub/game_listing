import linecache, logging, sys

from django.db import models

class Game(models.Model):
	title = models.CharField(max_length=1024, db_tablespace="indexes")
	platform = models.CharField(max_length=32)
	score = models.DecimalField(max_digits=16, decimal_places=6)
	genre = models.CharField(max_length=32)
	editors_choice = models.BooleanField(default=False)

	def __str__(self):
		return self.title
