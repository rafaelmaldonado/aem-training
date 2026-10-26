package com.example.assets.local.workflow;

import com.adobe.granite.workflow.WorkflowException;
import com.adobe.granite.workflow.WorkflowSession;
import com.adobe.granite.workflow.exec.WorkItem;
import com.adobe.granite.workflow.exec.WorkflowProcess;
import com.adobe.granite.workflow.metadata.MetaDataMap;
import com.day.cq.dam.api.Asset;
import com.day.cq.dam.api.Rendition;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Iterator;
import java.util.Calendar;
import javax.imageio.IIOImage;
import javax.imageio.ImageIO;
import javax.imageio.ImageReader;
import javax.imageio.ImageWriteParam;
import javax.imageio.ImageWriter;
import javax.imageio.stream.ImageInputStream;
import javax.jcr.Binary;
import javax.jcr.Node;
import javax.jcr.RepositoryException;
import javax.jcr.Session;
import javax.imageio.stream.ImageOutputStream;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.osgi.service.component.annotations.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(service = WorkflowProcess.class, property = "process.label=Local JPEG 800 rendition")
public class Jpeg800WorkflowProcess implements WorkflowProcess {
    static final String FOLDER = "/content/dam/assets";
    static final String RENDITION = "assets.800x800.jpeg";
    private static final String ORIGINAL_SUFFIX = "/jcr:content/renditions/original";
    private static final Logger LOG = LoggerFactory.getLogger(Jpeg800WorkflowProcess.class);

    @Override
    public void execute(WorkItem item, WorkflowSession session, MetaDataMap args) throws WorkflowException {
        if (!"JCR_PATH".equals(item.getWorkflowData().getPayloadType())) {
            return;
        }
        String path = assetPath(String.valueOf(item.getWorkflowData().getPayload()));
        if (path == null) {
            return;
        }
        ResourceResolver resolver = session.adaptTo(ResourceResolver.class);
        if (resolver == null) {
            throw new WorkflowException("No se pudo obtener el ResourceResolver del workflow");
        }
        Resource resource = resolver.getResource(path);
        Asset asset = resource == null ? null : resource.adaptTo(Asset.class);
        if (asset == null || asset.getMimeType() == null || !asset.getMimeType().startsWith("image/")) {
            return;
        }
        Rendition original = asset.getOriginal();
        if (original == null) {
            throw new WorkflowException("El asset todavía no tiene original: " + path);
        }
        try (InputStream source = original.getStream()) {
            byte[] jpeg = renderJpeg(source);
            if (jpeg == null) {
                LOG.warn("ImageIO no puede leer la imagen original: {}", path);
                return;
            }
            writeRendition(session.adaptTo(Session.class), path, jpeg);
            LOG.info("Rendition {} creada para {}", RENDITION, path);
        } catch (IOException | RepositoryException e) {
            throw new WorkflowException("No se pudo generar la rendition de " + path, e);
        }
    }

    private static void writeRendition(Session session, String assetPath, byte[] jpeg) throws RepositoryException {
        if (session == null) {
            throw new RepositoryException("No se pudo obtener la sesión JCR del workflow");
        }
        Node renditions = session.getNode(assetPath + "/jcr:content/renditions");
        Node file = renditions.hasNode(RENDITION)
                ? renditions.getNode(RENDITION) : renditions.addNode(RENDITION, "nt:file");
        Node content = file.hasNode("jcr:content")
                ? file.getNode("jcr:content") : file.addNode("jcr:content", "nt:resource");
        Binary binary = session.getValueFactory().createBinary(new ByteArrayInputStream(jpeg));
        try {
            content.setProperty("jcr:data", binary);
            content.setProperty("jcr:mimeType", "image/jpeg");
            content.setProperty("jcr:lastModified", Calendar.getInstance());
            session.save();
        } finally {
            binary.dispose();
        }
    }

    static String assetPath(String payload) {
        String path = payload.endsWith(ORIGINAL_SUFFIX)
                ? payload.substring(0, payload.length() - ORIGINAL_SUFFIX.length()) : payload;
        return path.startsWith(FOLDER + "/") ? path : null;
    }

    static byte[] renderJpeg(InputStream input) throws IOException {
        BufferedImage original = readImage(input);
        if (original == null) {
            return null;
        }
        double scale = Math.min(1.0, Math.min(800.0 / original.getWidth(), 800.0 / original.getHeight()));
        int width = Math.max(1, (int) Math.round(original.getWidth() * scale));
        int height = Math.max(1, (int) Math.round(original.getHeight() * scale));
        BufferedImage resized = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics2D graphics = resized.createGraphics();
        try {
            graphics.setColor(Color.WHITE);
            graphics.fillRect(0, 0, width, height);
            graphics.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC);
            graphics.drawImage(original, 0, 0, width, height, null);
        } finally {
            graphics.dispose();
        }
        Iterator<ImageWriter> writers = ImageIO.getImageWritersByMIMEType("image/jpeg");
        if (!writers.hasNext()) {
            throw new IOException("No hay codificador JPEG disponible");
        }
        ImageWriter writer = writers.next();
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        try (ImageOutputStream imageOutput = ImageIO.createImageOutputStream(output)) {
            writer.setOutput(imageOutput);
            ImageWriteParam params = writer.getDefaultWriteParam();
            params.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
            params.setCompressionQuality(0.85f);
            writer.write(null, new IIOImage(resized, null, null), params);
        } finally {
            writer.dispose();
        }
        return output.toByteArray();
    }

    private static BufferedImage readImage(InputStream input) throws IOException {
        try (ImageInputStream imageInput = ImageIO.createImageInputStream(input)) {
            if (imageInput == null) {
                throw new IOException("No se pudo abrir la imagen original");
            }
            Iterator<ImageReader> readers = ImageIO.getImageReaders(imageInput);
            IOException failure = null;
            while (readers.hasNext()) {
                ImageReader reader = readers.next();
                try {
                    imageInput.seek(0);
                    reader.setInput(imageInput);
                    return reader.read(0);
                } catch (IOException | RuntimeException e) {
                    // The SDK registers a JPEG reader that fails under Java 21; try the next provider.
                    failure = new IOException("El lector de imágenes no pudo procesar el original", e);
                } finally {
                    reader.dispose();
                }
            }
            if (failure != null) {
                throw failure;
            }
            return null;
        }
    }
}
