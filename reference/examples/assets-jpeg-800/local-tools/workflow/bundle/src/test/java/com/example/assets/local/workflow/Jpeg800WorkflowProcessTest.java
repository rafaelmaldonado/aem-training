package com.example.assets.local.workflow;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import javax.imageio.ImageIO;
import org.junit.jupiter.api.Test;

class Jpeg800WorkflowProcessTest {
    @Test
    void acceptsOnlyAssetsInConfiguredFolder() {
        assertEquals("/content/dam/assets/products/photo.png", Jpeg800WorkflowProcess.assetPath(
                "/content/dam/assets/products/photo.png/jcr:content/renditions/original"));
        assertNull(Jpeg800WorkflowProcess.assetPath("/content/dam/assets-other/photo.png"));
        assertNull(Jpeg800WorkflowProcess.assetPath("/content/dam/other/photo.png"));
    }

    @Test
    void createsJpegWithinEightHundredPixelBox() throws Exception {
        BufferedImage source = new BufferedImage(1600, 600, BufferedImage.TYPE_INT_ARGB);
        ByteArrayOutputStream png = new ByteArrayOutputStream();
        ImageIO.write(source, "png", png);

        byte[] jpeg = Jpeg800WorkflowProcess.renderJpeg(new ByteArrayInputStream(png.toByteArray()));
        BufferedImage result = ImageIO.read(new ByteArrayInputStream(jpeg));
        assertEquals(800, result.getWidth());
        assertEquals(300, result.getHeight());
    }
}
