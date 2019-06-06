package nl.knokko.quick;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.util.Random;

/**
 * Converts images to graphs
 * @author Tim van de Klundert
 *
 */
public class ImageToGraphConverter {
	
	private static final byte SEMICOLON = (byte) ';';
	private static final byte LINE_SEPARATOR = (byte) '\n';
	private static final byte ZERO = (byte) '0';

	public static void generate(String NAME, BufferedImage source) throws IOException {
		if (source.getWidth() != source.getHeight()) {
			throw new IllegalArgumentException("Width must be equal to height");
		}
		final int VERTICES = source.getWidth();
		OutputStream output = Files.newOutputStream(new File(NAME + ".csv").toPath());
		byte[] vertexNames = new byte[VERTICES * 10];
		Random random = new Random();
		for (int index = 0; index < vertexNames.length; index++) {
			vertexNames[index] = (byte) ('a' + random.nextInt(26));
		}
		
		byte[] line = new byte[2 + 11 * VERTICES];
		line[line.length - 1] = LINE_SEPARATOR;
		for (int index = 0; index < VERTICES; index++) {
			System.arraycopy(vertexNames, index * 10, line, 1 + index * 11, 10);
			line[index * 11] = SEMICOLON;
		}
		output.write(line);
		
		byte[] buffer = new byte[12 + 4 * VERTICES];
		
		for (int rowIndex = 0; rowIndex < VERTICES; rowIndex++) {
			System.arraycopy(vertexNames, rowIndex * 10, buffer, 0, 10);
			int bufferIndex = 10;
			for (int columnIndex = 0; columnIndex < VERTICES; columnIndex++) {
				buffer[bufferIndex++] = SEMICOLON;
				Color pixel = new Color(source.getRGB(columnIndex, rowIndex));
				int weight = (pixel.getRed() + pixel.getGreen() + pixel.getBlue() + 5) * pixel.getAlpha() / 256;
				if (weight >= 100) {
					buffer[bufferIndex++] = (byte) (ZERO + weight / 100);
				}
				if (weight >= 10) {
					buffer[bufferIndex++] = (byte) (ZERO + (weight % 100) / 10);
				}
				buffer[bufferIndex++] = (byte) (ZERO + weight % 10);
			}
			buffer[bufferIndex++] = SEMICOLON;
			buffer[bufferIndex++] = LINE_SEPARATOR;
			output.write(buffer, 0, bufferIndex);
		}
		
		output.flush();
		output.close();
	}
}