/*
 * Tim van de Klundert
 * 
 * Created at 08-05-2019
 * Last modified at 23-05-2019
 */
package nl.knokko.quick;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.Random;

public class GraphGenerator {
	
	private static final byte SEMICOLON = (byte) ';';
	private static final byte LINE_SEPARATOR = (byte) '\n';
	private static final byte ZERO = (byte) '0';
	private static final byte DOT = (byte) '.';

	public static void generate(int VERTICES, int EDGES, String NAME, int intDigits, int fractDigits) throws IOException {
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
		
		int bytesPerEdge = 2 + intDigits + fractDigits;
		byte[] buffer = new byte[12 + bytesPerEdge * VERTICES];
		boolean[] selectionBuffer = new boolean[VERTICES];
		int[] permutationBuffer = new int[VERTICES];
		int edgesSoFar = 0;
		int[] degrees = new int[VERTICES];
		for (int rowIndex = 0; rowIndex < VERTICES; rowIndex++) {
			final int edgesLeft = EDGES - edgesSoFar;
			
			// Including this row
			final int rowsLeft = VERTICES - rowIndex;
			final int minEdgesThisRow = edgesLeft - (rowsLeft - 1) * VERTICES;
			int edgesThisRow = edgesLeft / rowsLeft;
			if (edgesThisRow != 0) {
				edgesThisRow = edgesThisRow / 2 + random.nextInt(edgesThisRow);
				if (edgesThisRow > VERTICES) {
					edgesThisRow = VERTICES;
				}
			}
			if (edgesThisRow > edgesLeft) {
				edgesThisRow = edgesLeft;
			} else if (edgesThisRow < minEdgesThisRow) {
				edgesThisRow = minEdgesThisRow;
			}
			edgesSoFar += edgesThisRow;
			degrees[rowIndex] = edgesThisRow;
		}
		int[] degreeMix = new int[VERTICES];
		int[] newDegrees = Arrays.copyOf(degrees, VERTICES);
		randomPermutation(degreeMix, random, VERTICES, VERTICES);
		for (int index = 0; index < VERTICES; index++) {
			newDegrees[index] = degrees[degreeMix[index]];
		}
		degrees = newDegrees;
		int degreeSum = 0;
		for (int degree : degrees) {
			degreeSum += degree;
		}
		if (degreeSum != EDGES) {
			throw new Error("degreeSum is " + degreeSum + " and EDGES is " + EDGES);
		}
		
		
		for (int rowIndex = 0; rowIndex < VERTICES; rowIndex++) {
			System.arraycopy(vertexNames, rowIndex * 10, buffer, 0, 10);
			putSelection(random, selectionBuffer, degrees[rowIndex], permutationBuffer);
			int bufferIndex = 10;
			for (int columnIndex = 0; columnIndex < VERTICES; columnIndex++) {
				buffer[bufferIndex++] = SEMICOLON;
				if (selectionBuffer[columnIndex]) {
					if (intDigits > 0) {
						for (int digit = 0; digit < intDigits; digit++) {
							buffer[bufferIndex++] = (byte) ('1' + random.nextInt(9));
						}
					} else {
						buffer[bufferIndex++] = ZERO;
					}
					if (fractDigits > 0) {
						buffer[bufferIndex++] = DOT;
						for (int digit = 0; digit < fractDigits; digit++) {
							buffer[bufferIndex++] = (byte) ('1' + random.nextInt(9));
						}
					}
				} else {
					buffer[bufferIndex++] = ZERO;
				}
			}
			buffer[bufferIndex++] = SEMICOLON;
			buffer[bufferIndex++] = LINE_SEPARATOR;
			output.write(buffer, 0, bufferIndex);
		}
		
		output.flush();
		output.close();
	}
	
	static void putSelection(Random random, boolean[] dest, int trues, int[] permutationBuffer) {
		int falses = dest.length - trues;
		if (trues > falses) {
			Arrays.fill(dest, true);
			randomPermutation(permutationBuffer, random, falses, dest.length);
			for (int index = 0; index < falses; index++) {
				dest[permutationBuffer[index]] = false;
			}
		} else {
			Arrays.fill(dest, false);
			randomPermutation(permutationBuffer, random, trues, dest.length);
			for (int index = 0; index < trues; index++) {
				dest[permutationBuffer[index]] = true;
			}
		}
	}
	
	static void randomPermutation(int[] permutationBuffer, Random random, int size, int maxValue) {
		for (int index = 0; index < maxValue; index++) {
			permutationBuffer[index] = index;
		}
		for (int index = 0; index < size; index++) {
			int old = permutationBuffer[index];
			int otherIndex = index + random.nextInt(maxValue - index);
			permutationBuffer[index] = permutationBuffer[otherIndex];
			permutationBuffer[otherIndex] = old;
		}
	}
	
	static String randomName(Random random) {
		char[] name = new char[10];
		for (int index = 0; index < name.length; index++) {
			name[index] = (char) ('a' + random.nextInt(26));
		}
		return new String(name);
	}
}