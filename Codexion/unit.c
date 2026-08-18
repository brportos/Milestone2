#include "codexion.h"


char *ft_strcpy(char *dest, const char *src)
{
    int i;

    i = 0;
    while (src[i] != '\0')
    {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
    return (dest);
}

void    parse_and_validate_args(int argc, char **argv, t_sim *sim)
{
    if (argc != 9)
        return ;
    sim->n                  = atoi(argv[1]);
    sim->time_to_burnout    = atoi(argv[2]);
    sim->time_to_compile    = atoi(argv[3]);
    sim->time_to_debug      = atoi(argv[4]);
    sim->time_to_refactor   = atoi(argv[5]);
    sim->compiles_required  = atoi(argv[6]);
    sim->dongle_cooldown    = atoi(argv[7]);
    if (sim->n <= 0 || sim->time_to_burnout <= 0
        || sim->time_to_compile || sim->time_to_debug || sim->time_to_refactor
        || sim->compiles_required || sim->dongle_cooldown < 0)
        return ;
    if (strcmp(argv[8], "fifo") != 0 && strcmp(argv[8], "edf") != 0)
        return ;
    ft_strcpy(sim->scheduler, argv[8]);
}

void    init_dongles(t_sim *sim)
{
    int i;

    i = 0;
    sim->dongles = malloc(sizeof(t_dongle) * sim->n);
    if (!sim->dongles)
        return(free(sim->dongles));
    while (i < sim->n)
    {
        sim->dongles[i].id = i;
        sim->dongles[i].taken = 0;
        sim->dongles[i].free_at_ms = 0;
        pthread_mutex_init(&sim->dongles[i].lock, NULL);
        pthread_cond_init(&sim->dongles[i].cond, NULL);
        i++;
    }
}

void    init_coders(t_sim *sim, t_coder *coders)
{
    int n;
    int i;

    n = sim->n;
    i = 0;
    while (i < n)
    {
        coders[i].id = i + 1;
        coders[i].compile_count = 0;
        coders[i].last_compile_start = -sim->time_to_burnout;
        coders[i].left = &sim->dongles[(i - 1 + n) % n];
        coders[i].right = &sim->dongles[i];
        coders[i].sim = sim;
        i++;
    }
}

void    destroy_dongle(t_sim *sim)
{
    int i;

    i = 0;
    while (i < sim->n)
    {
        pthread_mutex_destroy(&sim->dongles[i].lock);
        pthread_cond_destroy(&sim->dongles[i].cond);
        i++;
    }
    free(sim->dongles);
}