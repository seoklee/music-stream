from django.db import models
from django.db.models import Model
from django.template.defaultfilters import slugify
from os.path import splitext
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, COMM, TALB


class Song(models.Model):
	owner = models.CharField(max_length=30,default=None)
	file_name = models.CharField(max_length=128,unique=True)
	songfile = models.FileField(upload_to='music/%Y/%m/%d')
	title = models.CharField(max_length=128,default='untitled')
	artist = models.CharField(max_length=128,default='unknown')
	album = models.CharField(max_length=128,default='unknown')
	track_num = models.PositiveSmallIntegerField(default=1)
	length = models.PositiveSmallIntegerField(default=0)
	artist_slug = models.SlugField(max_length=128,default='unknown')
	album_slug = models.SlugField(max_length=128,default='unknown')


	def __unicode__(self):
			return self.file_name

	def save(self, *args, **kwargs):
		self.file_name = splitext(self.file_name)[0]
		super(Song,self).save(*args, **kwargs)

	def update(self):
		audiofile = ID3(self.songfile.path)
		mp3file = MP3(self.songfile.path)
		self.title = audiofile["TIT2"]
		self.artist = audiofile["TPE1"]
		self.album = audiofile["TALB"]
		self.artist_slug = slugify(self.artist)
		self.album_slug = slugify(self.album)
		tmp = mp3file.info.length
		tmp = str(tmp).split(".",1)
		self.length = tmp[0]
		tmp = audiofile["TRCK"]
		tmp = str(tmp).split("/",1)
		self.track_num = tmp[0]
		super(Song,self).save();

		