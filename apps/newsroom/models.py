import uuid
from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    content = models.TextField(help_text='Supports **bold**, _italic_, and [links](url). Paragraphs separated by blank lines.')
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'newsroom_blogpost'
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def parsed_content(self):
        """Convert simple markdown-like markup to HTML."""
        import re
        lines = self.content.split('\n')
        html_parts = []
        paragraph = []

        for line in lines:
            if line.strip() == '':
                if paragraph:
                    text = ' '.join(paragraph)
                    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
                    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
                    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
                    html_parts.append(f'<p>{text}</p>')
                    paragraph = []
            else:
                paragraph.append(line.strip())

        if paragraph:
            text = ' '.join(paragraph)
            import re
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
            text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
            html_parts.append(f'<p>{text}</p>')

        return '\n'.join(html_parts)
