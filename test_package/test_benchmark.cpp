#include <benchmark/benchmark.h>

void TestBenchmark(benchmark::State& state) {
  for (auto _ : state) {
    benchmark::DoNotOptimize(state.iterations());
  }
}

BENCHMARK(TestBenchmark);

BENCHMARK_MAIN();
