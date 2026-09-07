NAME = codexion

CC = cc -g
CFLAGS = -Wall -Wextra -Werror


SRC = coders.c \
	main.c \
	dongle.c \
	arg.c \
	frees.c \
	init.c \
	simul.c \
	heap.c \
	scheduler.c \
	utils.c \
	burnout.c \
	display.c \
	time.c \
	routine.c 

OBJ = $(SRC:%.c=%.o)

all: $(NAME)

%.o: %.c
	@$(CC) $(CFLAGS) -c $< -o $@

$(NAME): $(OBJ)
	@$(CC) $(CFLAGS) -o $@ $(OBJ) -pthread
	@echo "codexion is created"

clean:
	@rm -rf $(OBJ)

fclean: clean
	@rm -rf $(NAME)

re: fclean all

.PHONY: all clean fclean re