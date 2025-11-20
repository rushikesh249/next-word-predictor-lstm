#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <set>
#include <chrono>
#include <cmath>

// ---------------------- Tokenizer ----------------------
std::vector<std::string> tokenize(const std::string &text)
{
    std::stringstream ss(text);
    std::string token;
    std::vector<std::string> tokens;

    while (ss >> token)
    {
        // remove punctuation
        token.erase(std::remove_if(token.begin(), token.end(), ::ispunct), token.end());
        // lowercase
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
        std::cerr << "Error: dataset not found!" << std::endl;
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

// ---------------------- Build Next Word Mapping ----------------------
std::map<std::string, std::map<std::string, int>> buildMapping(const std::vector<std::string> &tokens)
{
    std::map<std::string, std::map<std::string, int>> next_word_freq;
    for (size_t i = 0; i + 1 < tokens.size(); i++)
    {
        next_word_freq[tokens[i]][tokens[i + 1]]++;
    }
    return next_word_freq;
}

// ---------------------- Compute Cross-Entropy Loss ----------------------
double computeLoss(const std::vector<std::string> &tokens,
                   std::map<std::string, std::map<std::string, int>> &next_word_freq)
{
    double loss = 0.0;
    int count = 0;

    for (size_t i = 0; i + 1 < tokens.size(); i++)
    {
        std::string current = tokens[i];
        std::string target = tokens[i + 1];

        auto &freq_map = next_word_freq[current];
        int total = 0;
        for (auto &p : freq_map)
            total += p.second;

        if (total > 0 && freq_map.find(target) != freq_map.end())
        {
            double prob = (double)freq_map[target] / total;
            loss -= std::log(prob + 1e-9); // avoid log(0)
            count++;
        }
    }

    return (count > 0) ? loss / count : 0.0;
}

// ---------------------- Training ----------------------
void trainModel(const std::vector<std::string> &tokens, int epochs)
{
    std::cout << "Training model (word frequency predictor)..." << std::endl;

    auto start = std::chrono::high_resolution_clock::now();

    std::map<std::string, std::map<std::string, int>> next_word_freq;

    for (int e = 1; e <= epochs; e++)
    {
        // Rebuild mapping in each epoch (simulating training passes)
        next_word_freq = buildMapping(tokens);

        // Compute loss
        double loss = computeLoss(tokens, next_word_freq);

        std::cout << "Epoch " << e << "/" << epochs
                  << " - Loss: " << loss << std::endl;
    }

    auto end = std::chrono::high_resolution_clock::now();
    double training_time = std::chrono::duration<double>(end - start).count();

    std::cout << "Training finished." << std::endl;
    std::cout << "Total training time: " << training_time << " seconds\n"
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

    // used words
    std::set<std::string> used_words(context.begin(), context.end());

    for (int step = 0; step < max_words; step++)
    {
        std::string last_word = context.back();
        std::string next_word = predictNextWord(last_word, next_word_freq, used_words);

        if (next_word.empty())
            break;

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
    // Load dataset
    std::string all_text = loadDataset("../data/dataset_10000.txt");

    // Tokenize dataset
    auto tokens = tokenize(all_text);

    // Train for 30 epochs with real timing
    trainModel(tokens, 30);

    // Build mapping once for prediction
    auto next_word_freq = buildMapping(tokens);

    // User input
    std::string user_input;
    std::cout << "Enter a starting phrase: ";
    std::getline(std::cin, user_input);

    // Generate sentence
    std::string sentence = generateSentence(user_input, next_word_freq, 15);

    std::cout << "\nFinal generated sentence: " << sentence << std::endl;

    return 0;
}
