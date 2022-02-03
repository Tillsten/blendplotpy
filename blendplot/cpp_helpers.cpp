#include <vector>
#include <optional>
#include "blend2d.h"

void make_path(const std::vector<float> &x, const std::vector<float> &y, BLPath &p)
{
    int n = x.size();
    p.reserve(n + 10);
    p.moveTo(x[0], y[0]);
    for (int i = 1; i < n; i++)
    {
        p.lineTo(x[i], y[i]);
    };
}

void make_scatter_path(const std::vector<float> &x, const std::vector<float> &y, BLPath &p, const BLPath &symbol)
{
    int n = x.size();
    p.reserve(n + 10);
    
    for (int i = 0; i < n; i++)
    {
        p.addPath(symbol, BLPoint(x[i], y[i]));
    };
}

std::vector<double> calculate_ticks(const double left, const double right, const double size, std::optional<int> num_ticks = std::nullopt)
{
    using namespace std;

    std::vector<double> out{};
    double min = std::min(left, right);
    double max = std::max(left, right);
    double range = max - min;

    if (!isfinite(range))
    {
        return out;
    }
    num_ticks = num_ticks.value_or(floor(size * 2));
    double exponent = log10(abs(range));
    double magnitude = pow(10, floor(exponent) - 1);
    double right_scaled = floor(max / magnitude);
    double left_scaled = ceil(min / magnitude);
    const std::array<double, 5> steps = {1, 2, 2.5, 5, 10};
    int step_ticks;
    double step_taken = NAN;
    for (const double &s : steps)
    {
        step_ticks = ceil((right_scaled - left_scaled) / s);
        if (step_ticks <= num_ticks)
        {
            step_taken = s;
            break;
        }
    }

    if (std::isnan(step_taken))
    {
        return out;
    };

    for (int i = 0; i <= step_ticks; i++)
    {
        double tick = left_scaled * magnitude + i * magnitude * step_taken;
        if (tick < max)
        {
            out.push_back(left_scaled * magnitude + i * magnitude * step_taken);
        }
        else
        {
            break;
        }
    }
    return out;
}

