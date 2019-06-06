package nl.knokko.gui;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import nl.knokko.gui.color.GuiColor;
import nl.knokko.gui.color.SimpleGuiColor;
import nl.knokko.gui.component.menu.FileChooserMenu;
import nl.knokko.gui.component.menu.GuiMenu;
import nl.knokko.gui.component.text.TextButton;
import nl.knokko.gui.component.text.TextComponent;
import nl.knokko.gui.util.TextBuilder.Properties;
import nl.knokko.gui.window.AWTGuiWindow;
import nl.knokko.gui.window.GuiWindow;
import nl.knokko.quick.ImageToGraphConverter;

/**
 * A quick tool to convert images to graphs. It was made to help us win the aesthetics award.
 * It uses github.com/knokko/Gui as library to quickly make this menu.
 * @author Tim van de Klundert
 *
 */
public class GraphGui {

	public static void main(String[] args) {
		GuiWindow window = new AWTGuiWindow();
		window.open("Image to Graph converter", true);
		window.setMainComponent(new Menu());
		window.run(20);
	}
	
	static final Properties ERROR_PROPS = Properties.createLabel(Color.red);
	static final Properties INFO_PROPS = Properties.createLabel();
	static final Properties BUTTON_PROPS = Properties.createButton(new Color(0,0,200), new Color(0,0,40));
	static final Properties HOVER_PROPS = Properties.createButton(new Color(0,0,255), new Color(0,0,50));
	
	static class Menu extends GuiMenu {
		
		@Override
		public GuiColor getBackgroundColor() {
			return SimpleGuiColor.GREEN;
		}

		@Override
		protected void addComponents() {
			TextComponent errorComponent = new TextComponent("", ERROR_PROPS);
			addComponent(errorComponent, 0.05f, 0.91f, 0.95f, 0.97f);
			FileChooserMenu chooser = new FileChooserMenu(this, (File file) -> {
				try {
					BufferedImage image = ImageIO.read(file);
					if (image.getWidth() == image.getHeight()) {
						long startTime = System.currentTimeMillis();
						ImageToGraphConverter.generate(file.getName(), image);
						long endTime = System.currentTimeMillis();
						errorComponent.setDirectText("Took " + (endTime - startTime) + " ms");
						errorComponent.setProperties(INFO_PROPS);
					} else {
						errorComponent.setText("The image (" + image.getWidth() + ") should be equal to the height (" + image.getHeight() + ")");
					}
				} catch (IOException ioex) {
					errorComponent.setText(ioex.getMessage());
				}
			}, (File file) -> {
				String[] suffixes = ImageIO.getReaderFileSuffixes();
				for (String suffix : suffixes) {
					if (file.getName().endsWith(suffix)) {
						return true;
					}
				}
				return false;
			});
			addComponent(new TextButton("Choose image...", BUTTON_PROPS, HOVER_PROPS, () -> {
				state.getWindow().setMainComponent(chooser);
			}), 0.15f, 0.5f, 0.35f, 0.6f);
		}
	}
}