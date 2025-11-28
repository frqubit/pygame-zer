pygame\_zer package
===================

pygame\_zer allows you to add zoomable and explorable regions to your
pygame window. Once a driver is created, you can display its contents
and pan/zoom around the world.

Everything starts from the Driver class. Once a driver is made, other
objects can be added to it using their constructors. Everything else
is handled internally.

.. code-block:: python

    import pygame
    import pygame_zer

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    driver = pygame_zer.Driver(screen)

    pygame_zer.Rect(driver, (50, 50, 100, 100))
    pygame_zer.Circle(driver, (100, 100), 25, fill="red")

    running = True
    while running:
        for event in pygame.event.get():
            if driver.handle_event(event):
                continue
            if event.type == pygame.QUIT:
                running = False

        screen.fill((50, 50, 50))
        driver.draw()

        pygame.display.flip()

    pygame.quit()

Some things are automatically exported by the default
module import. These include:

* Circle:
  :py:class:`pygame_zer.circle.Circle`
* Image:
  :py:class:`pygame_zer.image.Image`
* Line:
  :py:class:`pygame_zer.line.Line`
* Rect:
  :py:class:`pygame_zer.rect.Rect`
* Text:
  :py:class:`pygame_zer.text.Text`

* Driver:
  :py:class:`pygame_zer.driver.Driver`

Flags: :py:class:`pygame_zer.driver.DriverFlags`

* F_EMPTY
* F_ZOOMABLE
* F_EXPLORABLE
* F_NOCACHE
* F_DEFAULT

Please see the GitHub repository for more examples.

.. automodule:: pygame_zer.camera
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.circle
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.driver
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.image
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.line
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.rect
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.shape
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.text
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer.types
   :members:
   :show-inheritance:
   :undoc-members:

.. automodule:: pygame_zer
   :members:
   :show-inheritance:
   :undoc-members:
