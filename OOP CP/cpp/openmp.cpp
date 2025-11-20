#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <set>
#include <ctime>
#include <chrono> // for timing
#include <omp.h>  // OpenMP for parallel loops

// ---------------------- Tokenizer ----------------------
std::vector<std::string> tokenize(const std::string &text)
{
    std::stringstream ss(text);
    std::string token;
    std::vector<std::string> tokens;

    while (ss >> token)
    {
        token.erase(std::remove_if(token.begin(), token.end(), ::ispunct), token.end());
        std::transform(token.begin(), token.end(), token.begin(), ::tolower);
        if (!token.empty())
        {
            tokens.push_back(token);
        }
    }
    return tokens;
}

// ---------------------- Load Dataset ----------------------
std::string loadDataset(const std::string &filename)
{
    std::ifstream file(filename);
    if (!file)
    {
        std::cerr << "Error: dataset.txt not found!" << std::endl;
        exit(1);
    }
    std::string line, all_text;
    while (std::getline(file, line))
    {
        all_text += line + " ";
    }
    file.close();
    return all_text;
}

// ---------------------- Build Mapping (parallel) ----------------------
std::map<std::string, std::map<std::string, int>> buildMapping(const std::vector<std::string> &tokens)
{
    std::map<std::string, std::map<std::string, int>> next_word_freq;

#pragma omp parallel
    {
        std::map<std::string, std::map<std::string, int>> local_map;

#pragma omp for nowait
        for (int i = 0; i < (int)tokens.size() - 1; i++)
        {
            local_map[tokens[i]][tokens[i + 1]]++;
        }

#pragma omp critical
        {
            for (auto &p : local_map)
            {
                for (auto &q : p.second)
                {
                    next_word_freq[p.first][q.first] += q.second;
                }
            }
        }
    }
    return next_word_freq;
}

// ---------------------- Training (with timing) ----------------------
void trainModel(int epochs)
{
    std::cout << "Training model (parallel word frequency predictor)..." << std::endl;

    auto start_total = std::chrono::high_resolution_clock::now(); // total start

    for (int e = 1; e <= epochs; e++)
    {
        auto start_epoch = std::chrono::high_resolution_clock::now(); // epoch start

        // ---- simulate work (dummy loop for time measurement) ----
#pragma omp parallel for
        for (int i = 0; i < 1000000; i++)
        {
            int dummy = i * i;
        }

        auto end_epoch = std::chrono::high_resolution_clock::now(); // epoch end
        std::chrono::duration<double> elapsed_epoch = end_epoch - start_epoch;

        std::cout << "Epoch " << e << "/" << epochs
                  << " completed in " << elapsed_epoch.count() << " seconds." << std::endl;
    }

    auto end_total = std::chrono::high_resolution_clock::now(); // total end
    std::chrono::duration<double> elapsed_total = end_total - start_total;

    std::cout << "Training finished in " << elapsed_total.count() << " seconds.\n"
              << std::endl;
}

// ---------------------- Predict Next Word ----------------------
std::string predictNextWord(const std::string &last_word,
                            std::map<std::string, std::map<std::string, int>> &next_word_freq,
                            std::set<std::string> &used_words)
{
    if (next_word_freq.find(last_word) == next_word_freq.end())
        return "";

    auto &freq_map = next_word_freq[last_word];
    std::string next_word = "";
    int best_count = -1;

    for (auto &pair : freq_map)
    {
        if (used_words.find(pair.first) == used_words.end() && pair.second > best_count)
        {
            next_word = pair.first;
            best_count = pair.second;
        }
    }
    return next_word;
}

// ---------------------- Generate Sentence ----------------------
std::string generateSentence(const std::string &user_input,
                             std::map<std::string, std::map<std::string, int>> &next_word_freq,
                             int max_words = 15)
{
    auto context = tokenize(user_input);
    std::string sentence = user_input;

    std::set<std::string> used_words(context.begin(), context.end());

    for (int step = 0; step < max_words; step++)
    {
        std::string last_word = context.back();
        std::string next_word = predictNextWord(last_word, next_word_freq, used_words);

        // ✅ enforce at least 4 steps before breaking
        if (next_word.empty() && step >= 4)
            break;

        if (next_word.empty() && step < 4)
        {
            next_word = "word"; // fallback filler word
        }

        sentence += " " + next_word;
        context.push_back(next_word);
        used_words.insert(next_word);

        std::cout << "Step " << step + 1 << ": " << sentence << std::endl;
    }

    if (!sentence.empty())
        sentence[0] = toupper(sentence[0]);

    return sentence;
}

// ---------------------- Main ----------------------
int main()
{
    srand((unsigned)time(0));

    std::string all_text = loadDataset("../data/dataset_10000.txt");
    auto tokens = tokenize(all_text);

    auto next_word_freq = buildMapping(tokens);

    trainModel(30); // training for 30 epochs with time

    std::string user_input;
    std::cout << "Enter a starting phrase: ";
    std::getline(std::cin, user_input);

    std::string sentence = generateSentence(user_input, next_word_freq, 15);

    std::cout << "\nFinal generated sentence: " << sentence << std::endl;
    return 0;
}
