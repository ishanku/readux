"""
Test class for manage command to rebuild OCR
"""
from io import StringIO
from bs4 import BeautifulSoup
from django.test import TestCase
from django.core.management import call_command
from ...canvases.models import Canvas, IServer
from .factories import CanvasFactory

class CanvasTests(TestCase):
    fixtures = ['kollections.json', 'manifests.json', 'canvases.json', 'annotations.json']

    def setUp(self):
        self.canvas = Canvas.objects.get(pk='7261fae2-a24e-4a1c-9743-516f6c4ea0c9')

    def test_command_output_rebuild_manifest(self):
        # manifest = Manifest.objects
        out = StringIO()
        call_command('rebuild_ocr', manifest=self.canvas.manifest.pid, stdout=out)
        assert 'OCR rebuilt for manifest' in out.getvalue()

    def test_command_output_rebuild_canvas(self):
        out = StringIO()
        call_command('rebuild_ocr', canvas=Canvas.objects.all().first().pid, stdout=out)
        assert 'OCR rebuilt for canvas' in out.getvalue()

    def test_command_output_rebuild_canvas_with_no_existing_annotations(self):
        canvas = CanvasFactory.create(manifest=self.canvas.manifest)
        out = StringIO()
        call_command('rebuild_ocr', canvas=canvas.pid, stdout=out)
        assert 'OCR rebuilt for canvas' in out.getvalue()

    def test_command_output_rebuild_canvas_not_found(self):
        out = StringIO()
        call_command('rebuild_ocr', canvas='barco', stdout=out)
        assert 'ERROR: canvas not found' in out.getvalue()

    def test_command_output_rebuild_manifest_not_found(self):
        out = StringIO()
        call_command('rebuild_ocr', manifest='josef', stdout=out)
        assert 'ERROR: manifest not found' in out.getvalue()

    def test_command_output_rebuild_pid_not_given(self):
        out = StringIO()
        call_command('rebuild_ocr', stdout=out)
        assert 'ERROR: your must provide a manifest or canvas pid' in out.getvalue()

    def test_command_rebuild_ocr_canvas(self):
        original_anno_count = self.canvas.annotation_set.all().count()
        # Check the OCR attributes before rebuilding.
        first_anno = self.canvas.annotation_set.all().first()
        assert first_anno.h == 22
        assert first_anno.w == 22
        assert first_anno.x == 1146
        assert first_anno.y == 928
        original_span = BeautifulSoup(first_anno.content, 'html.parser')
        assert 'Dope' not in original_span.string
        assert original_span.span is not None
        assert original_span.span.span is None
        self.canvas.IIIF_IMAGE_SERVER_BASE = IServer.objects.get(
            IIIF_IMAGE_SERVER_BASE='http://fake.info'
        )
        self.canvas.save()
        out = StringIO()
        call_command('rebuild_ocr', canvas=self.canvas.pid, testing=True, stdout=out)
        assert 'OCR rebuilt for canvas' in out.getvalue()
        ocr = self.canvas.annotation_set.all().first()
        assert ocr.h == 22
        assert ocr.w == 22
        assert ocr.x == 1146
        assert ocr.y == 928
        new_span = BeautifulSoup(ocr.content, 'html.parser')
        assert 'Dope' in new_span.string
        assert original_span.string not in new_span.string
        assert new_span.span is not None
        assert new_span.span.span is None
        assert len(self.canvas.annotation_set.all()) == original_anno_count + 1

    def test_command_rebuild_ocr_manifest(self):
        canvas = Canvas.objects.get(pk='a7f1bd69-766c-4dd4-ab66-f4051fdd4cff')
        original_anno_count = canvas.annotation_set.all().count()
        # Check the OCR attributes before rebuilding.
        first_anno = canvas.annotation_set.all().first()
        assert first_anno.h == 22
        assert first_anno.w == 22
        assert first_anno.x == 1146
        assert first_anno.y == 928
        original_span = BeautifulSoup(first_anno.content, 'html.parser')
        assert 'southernplayalisticadillacmuzik' not in original_span.string
        assert original_span.span is not None
        assert original_span.span.span is None
        canvas.IIIF_IMAGE_SERVER_BASE = IServer.objects.get(
            IIIF_IMAGE_SERVER_BASE='http://fake.info'
        )
        canvas.save()
        out = StringIO()
        call_command('rebuild_ocr', manifest=canvas.manifest.pid, testing=True, stdout=out)
        assert 'OCR rebuilt for manifest' in out.getvalue()
        ocr = canvas.annotation_set.all().first()
        assert ocr.h == 22
        assert ocr.w == 22
        assert ocr.x == 1146
        assert ocr.y == 928
        new_span = BeautifulSoup(ocr.content, 'html.parser')
        assert 'Dope' in new_span.string
        assert original_span.string not in new_span.string
        assert new_span.span is not None
        assert new_span.span.span is None
        assert len(canvas.annotation_set.all()) == original_anno_count + 1