// Copyright (C) 2022-2022  kcgen <kcgen@users.noreply.github.com>
// SPDX-License-Identifier: GPL-3.0-or-later

// Compiling tips:
//  g++ -std=c++17 -Wall -Wextra -Wpedantic -Weffc++ process.cpp
//  clang++ -std=c++17 -Weverything -Wno-c++98-compat process.cpp
//  clang-format --sort-includes -i --style=Microsoft process.cpp

#include <cassert>
#include <cstdio>
#include <filesystem>
#include <fstream>
#include <limits>
#include <list>
#include <numeric>
#include <optional>
#include <string>

// Generic container holding a list of the top N candidate items
template <class T> class TopN
{
  public:
    TopN() = delete;
    TopN(const size_t n, const T &init_item = {}) : items(n, init_item), default_item(init_item)
    {
        assert(!items.empty());
    }
    void Consider(const T &candidate)
    {
        auto it = items.begin();
        while (it != items.end())
        {
            if (*it < candidate)
            {
                items.insert(it, candidate);
                items.pop_back();
                break;
            }
            ++it;
        }
    }
    T Sum() const
    {
        return std::accumulate(items.begin(), items.end(), default_item);
    }

  private:
    std::list<T> items = {};
    const T default_item = {};
};

using calories_t = int;
using num_elves_t = uint16_t;
using top_calories_t = TopN<calories_t>;
using args_t = std::pair<std::ifstream, num_elves_t>;

static std::optional<args_t> parse_args(const int argc, char **argv)
{
    if (argc != 3)
    {
        printf("Usage: %s FILE N\n"
               "Where:\n"
               "  FILE:  Is the file holding the elves' list of calories.\n"
               "     N:  Report the calorie sum of the top N elves' holdings.\n",
               argv[0]);
        return {};
    }
    // Can we trust the input file?
    std::ifstream input_file(argv[1], std::ios::binary);
    if (!input_file.is_open())
    {
        printf("Error: The FILE %s is not available or can't be opened.\n", argv[1]);
        return {};
    }
    // Can we trust the number of top items to retain?
    const auto n = atoi(argv[2]);
    constexpr int min_n = {1};
    constexpr int max_n = {std::numeric_limits<num_elves_t>::max()};
    if (n < min_n || n > max_n)
    {
        printf("Error: N needs to be between %d and %d, inclusively.\n", min_n, max_n);
        return {};
    }
    return std::make_pair(std::move(input_file), static_cast<num_elves_t>(n));
}

static top_calories_t process_list(std::ifstream &input_file, const num_elves_t n)
{
    top_calories_t top_n_calories(n);

    calories_t calories = {};
    std::string line = {};
    while (getline(input_file, line))
    {
        if (!line.empty())
        {
            calories += std::stoi(line);
        }
        else
        {
            top_n_calories.Consider(calories);
            calories = {};
        }
    }
    return top_n_calories;
}

int main(int argc, char **argv)
{
    auto args = parse_args(argc, argv);
    if (!args)
    {
        return 1;
    }

    auto &[input_file, top_n] = *args;

    const auto top_n_calories = process_list(input_file, top_n);

    printf("Combined sum of the top %u elves' holdings: %d calories\n", top_n, top_n_calories.Sum());

    return 0;
}
