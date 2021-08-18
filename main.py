import pygame
import neat
from models import Car, Visualization

screen_width = 1500
screen_height = 800
generation = 0


def evolve(genomes, config):
    # Init my game
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 20)
    font = pygame.font.SysFont("Arial", 20)
    map_game = pygame.image.load("assets/map.png")

    # Init NEAT
    nets = []
    cars = []
    learning_rate = 10

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        # Init my cars
        cars.append(Car(map_game, "assets/car.png"))

    # Main loop
    global generation
    generation += 1
    is_search = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        # Input my data and get result from network
        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_data())
            i = output.index(max(output))
            if i == 0:
                car.angle += learning_rate
            else:
                car.angle -= learning_rate

        # Update car and fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if car.get_alive():
                remain_cars += 1
                car.update()
                genomes[i][1].fitness += car.get_distance()
                if genomes[i][1].fitness > 12000:
                    is_search = False

        # check
        if remain_cars == 0:
            break
        if not is_search:
            break

        # Drawing
        screen.blit(map_game, (0, 0))
        for car in cars:
            if car.get_alive():
                Visualization(car, screen).draw()
                screen.blit(car.get_surface(), car.get_point())

        text = generation_font.render(f'Generation: {str(generation)}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.left = 10
        text_rect.bottom = 30
        screen.blit(text, text_rect)

        text = font.render(f'Population: {str(remain_cars)}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.left = 10
        text_rect.bottom = 60
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick()


if __name__ == "__main__":
    # Set configuration file
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(evolve, 100)
