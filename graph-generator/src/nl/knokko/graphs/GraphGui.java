/*
 * Tim van de Klundert (knokko)
 * 
 * Created at 08-05-2019
 * Last modified at 23-05-2019
 * 
 * In order to compile this, you need to download github.com/knokko/Gui and add it to the build path
 */
package nl.knokko.graphs;

import java.awt.Color;
import java.io.IOException;

import nl.knokko.gui.color.GuiColor;
import nl.knokko.gui.color.SimpleGuiColor;
import nl.knokko.gui.component.menu.GuiMenu;
import nl.knokko.gui.component.text.IntEditField;
import nl.knokko.gui.component.text.TextButton;
import nl.knokko.gui.component.text.TextComponent;
import nl.knokko.gui.component.text.TextEditField;
import nl.knokko.gui.util.Option;
import nl.knokko.gui.util.TextBuilder.Properties;
import nl.knokko.gui.window.AWTGuiWindow;
import nl.knokko.gui.window.GuiWindow;
import nl.knokko.quick.GraphGenerator;

public class GraphGui {

	public static void main(String[] args) {
		GuiWindow window = new AWTGuiWindow();
		window.setMainComponent(new Menu());
		window.open("Graph Generator", true);
		window.run(60);
	}

	static Properties LABEL_PROPS = Properties.createLabel();
	static Properties ERROR_PROPS = Properties.createLabel(Color.RED);
	static Properties EDIT = Properties.createEdit();
	static Properties EDIT_HOVER = Properties.createEdit(Color.GREEN);
	static Properties BUTTON = Properties.createButton(new Color(0, 150, 0), new Color(0, 50, 0));
	static Properties BUTTON_HOVER = Properties.createButton(new Color(0, 255, 0), new Color(0, 80, 0));

	static class Menu extends GuiMenu {

		@Override
		public GuiColor getBackgroundColor() {
			return SimpleGuiColor.BLUE;
		}

		@Override
		protected void addComponents() {
			TextComponent info = new TextComponent("", LABEL_PROPS);
			addComponent(info, 0.05f, 0.9f, 0.95f, 0.97f);
			addComponent(new TextComponent("Number of vertices:", LABEL_PROPS), 0.1f, 0.8f, 0.3f, 0.87f);
			IntEditField vertices = new IntEditField(150, 1, EDIT, EDIT_HOVER);
			addComponent(vertices, 0.4f, 0.8f, 0.5f, 0.87f);
			addComponent(new TextComponent("Number of edges:", LABEL_PROPS), 0.1f, 0.7f, 0.3f, 0.77f);
			IntEditField edges = new IntEditField(1000, 0, EDIT, EDIT_HOVER);
			addComponent(edges, 0.4f, 0.7f, 0.5f, 0.77f);
			addComponent(new TextComponent("Integer digits for edge weight:", LABEL_PROPS), 0f, 0.6f, 0.3f, 0.67f);
			IntEditField intDigits = new IntEditField(1, 0, EDIT, EDIT_HOVER);
			addComponent(intDigits, 0.4f, 0.6f, 0.5f, 0.67f);
			addComponent(new TextComponent("Fraction digits for edge weight:", LABEL_PROPS), 0f, 0.5f, 0.3f, 0.57f);
			IntEditField fractDigits = new IntEditField(0, 0, EDIT, EDIT_HOVER);
			addComponent(fractDigits, 0.4f, 0.5f, 0.5f, 0.57f);
			addComponent(new TextComponent("Name:", LABEL_PROPS), 0.1f, 0.3f, 0.2f, 0.37f);
			TextEditField name = new TextEditField("", EDIT, EDIT_HOVER);
			addComponent(name, 0.3f, 0.3f, 0.5f, 0.37f);
			addComponent(new TextButton("Generate", BUTTON, BUTTON_HOVER, () -> {
				Option.Int edgeCount = edges.getInt();
				Option.Int vertexCount = vertices.getInt();
				Option.Int intPartDigits = intDigits.getInt();
				Option.Int fractPartDigits = fractDigits.getInt();
				if (!edgeCount.hasValue()) {
					info.setProperties(ERROR_PROPS);
					info.setText("The number of edges must be a non-negative integer smaller than 2^31");
				}
				else if (!vertexCount.hasValue()) {
					info.setProperties(ERROR_PROPS);
					info.setText("The number of vertices must be a positive integer smaller than 2^31");
				} else if (!intPartDigits.hasValue()) {
					info.setProperties(ERROR_PROPS);
					info.setText("The number of integer digits must be a non-negative integer smaller than 2^31");
				} else if (!fractPartDigits.hasValue()) {
					info.setProperties(ERROR_PROPS);
					info.setText("The number of fraction digits must be a non-negative integer smaller than 2^31");
				} else if (edgeCount.getValue() > vertexCount.getValue() * vertexCount.getValue()){
					info.setProperties(ERROR_PROPS);
					info.setText("The number of edges can be at most the square of the number of vertices (" + vertexCount.getValue() * vertexCount.getValue() + ")");
				} else {
					try {
						long startTime = System.currentTimeMillis();
						GraphGenerator.generate(vertexCount.getValue(), edgeCount.getValue(), name.getText(), intPartDigits.getValue(), fractPartDigits.getValue());
						long endTime = System.currentTimeMillis();
						info.setProperties(LABEL_PROPS);
						info.setText("Took " + (endTime - startTime) + " ms");
					} catch (IOException ioex) {
						info.setProperties(ERROR_PROPS);
						info.setText(ioex.getMessage());
					}
				}
			}), 0.2f, 0.1f, 0.4f, 0.17f);
		}
	}
}