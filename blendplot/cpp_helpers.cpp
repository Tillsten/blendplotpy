#include <vector>
#include <optional>
#include "blend2d.h"


template <typename T>
BLBox box_union(const T &a, const T &b)
{
    return BLBox(blMin(a.x0, b.x0), blMin(a.y0, b.y0),
                 blMax(a.x1, b.x1), blMax(a.y1, b.y1));
}

BLBox box_union(const std::vector<BLBox> &a)
{
    auto out = BLBox();
    for (auto &&i : a)
    {
        out = box_union(out, i);
    }
    return out;
}

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

void draw_scatter(BLContext &ctx, const BLPath &p, const std::vector<double> &x, const std::vector<double> &y, float size)
{
    auto transform = BLMatrix2D();
    BLMatrix2D::invert(transform, ctx.userMatrix());

    auto tp = BLPath(p);
    tp.transform(BLMatrix2D::makeScaling(size));
    auto scale = transform.mapVector(BLPoint(1, 1));
    tp.transform(BLMatrix2D::makeScaling(scale));

    for (size_t i = 0; i < x.size(); i++)
    {
        auto coords = transform.mapPoint(BLPoint(x[i], y[i]));
        ctx.translate(x[i], y[i]);
        ctx.fillPath(tp);
        ctx.strokePath(tp);
        ctx.translate(-x[i], -y[i]);
    }
}



enum HTextAlignment
{
    Left,
    HCenter,
    Right
};
enum VTextAlignment
{
    Top,
    VCenter,
    Bottom
};

struct TextProps
{
    HTextAlignment ha = Left;
    VTextAlignment va = Bottom;
    BLPoint pos;
};

void draw_txt(BLContext &ctx, BLPoint &pos, BLFont &font, char *text,
              HTextAlignment ha = HTextAlignment::HCenter)
{
    BLTextMetrics tm;
    BLGlyphBuffer gb;

    gb.setUtf8Text(text);
    font.shape(gb);
    font.getTextMetrics(gb, tm);
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
    const std::array<double, 5> steps =  {1.0, 2.0, 2.5, 5.0, 10.0};
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
