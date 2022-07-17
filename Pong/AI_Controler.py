import pygame
import neat
import pickle
import os
from .Options import *

from Pong.Pong_Controller import Pong_Controller


class AI_Controller:
    def __init__(self, name1=False, name2=False, cheat=False):
        self.cheat = cheat
        self.conf = self.cargar_conf()
        self.name1 = name1
        self.name2 = name2


    def eval_genomes(self, genomes, config):
        for gen, (genome_id, genome) in enumerate(genomes):
            genome.fitness = 0

        if not self.name2 and not self.cheat:
            for i, (genome_id1, genome1) in enumerate(genomes):
                for genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
                    game = Pong_Controller()
                    game.train_ai(genome1, genome2, config, True)

        else:
            for i, (genome_id1, genome1) in enumerate(genomes):

                if not self.cheat:
                    genome2 = self.get_genome(self.name2)
                    game = Pong_Controller()
                    game.train_ai(genome1, genome2, config, False)
                else:
                    game = Pong_Controller(True)
                    game.train_ai(genome1, False, config, False)

    def train(self):
        #p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-23")
        p = neat.Population(self.conf)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(50, filename_prefix="CheckPoints"))

        winner = p.run(self.eval_genomes, 1000)

        with open("Best_Genomes/" + str(self.name1), "wb") as f:
            pickle.dump(winner, f)

    def play(self):

        if not self.name2:
            lUser = False
            if self.name1:
                rUser = self.get_genome(self.name1)
            else:
                rUser = False
        else:
            lUser = self.get_genome(self.name1)
            rUser = self.get_genome(self.name2)

        game = Pong_Controller(cheat=self.cheat)
        game.play(lUser, rUser, self.conf)


    def cargar_conf(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "../config.txt")

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                             neat.DefaultStagnation,
                             config_path)
        return config

    def get_genome(self, name):
        dirr = "Best_Genomes/" + str(name)
        with open(dirr, "rb") as f:
            winner = pickle.load(f)
        return winner
