import matplotlib.pyplot as plt
from IPython import display
plt.ion()

def update(not_legal_moves, mean_not_legal_moves, winning_rounds):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Count')

    # Plot the data
    plt.plot(not_legal_moves, label='Not Legal Moves')
    plt.plot(mean_not_legal_moves, label='Mean Not Legal Moves')
    plt.plot(winning_rounds, label='Winning Rounds')
    plt.ylim(ymin=0)

    # Add text annotations
    plt.text(len(not_legal_moves) - 1, not_legal_moves[-1], 
             "(" + str(len(not_legal_moves) - 1) + ", " + str(not_legal_moves[-1]) + ")")
    plt.text(len(mean_not_legal_moves) - 1, mean_not_legal_moves[-1], 
             "(" + str(len(mean_not_legal_moves) - 1) + ", " + str(mean_not_legal_moves[-1]) + ")")
    plt.text(len(winning_rounds) - 1, winning_rounds[-1], 
             "(" + str(len(winning_rounds) - 1) + ", " + str(winning_rounds[-1]) + ")")

    # Add the legend
    plt.legend()

    plt.show(block=False)
    plt.pause(0.1)  # Pause to update the plot

