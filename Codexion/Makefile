NAME = codexion

CC = cc -g
CFLAGS = -Wall -Wextra -Werror


SRC = coders.c \
	main.c \
	dongle.c \
	arg.c \
	frees.c \
	init.c \
	stop.c \
	priority.c \
	scheduler.c \
	utils.c

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