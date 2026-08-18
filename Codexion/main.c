#include "codexion.h"


int main(int argc, char *argv[])
{
    t_coder *coders;
    t_sim   sim;
    pthread_t *threads;

    coders = NULL;
    threads = NULL;
    parse_and_validate_args(argc, argv, &sim);
    init_simulation(&sim);
    alloc_sim_data(&sim, &coders, &threads);
    run_threads(&sim, threads);
    return (0);    
}