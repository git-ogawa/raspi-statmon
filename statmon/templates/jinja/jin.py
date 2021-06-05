from jinja2 import Template
from jinja2 import Environment, BaseLoader
import json

def make_script():
    s = """
    <script>
        var chartColors = {
            red: 'rgb(255, 99, 132)',
            orange: 'rgb(255, 159, 64)',
            yellow: 'rgb(255, 205, 86)',
            green: 'rgb(75, 192, 192)',
            blue: 'rgb(54, 162, 235)',
            purple: 'rgb(153, 102, 255)',
            grey: 'rgb(231,233,237)'
        };
        var color = Chart.helpers.color;
        {% raw %}
        function readJson() {
            var json = $.ajax({
                url: "{{ url_for('static', filename='settings/user_settings.json') }}",
                dataType: 'json',
                async: false
            }).responseText;
                return JSON.parse(json);
        }
        {% endraw %}
        var graph = readJson();
        let json_data;
        function get_data(){
            $.ajax({
                url: "/chart-data",
                method: "POST",
            })
            .done(function(data){
                json_data = JSON.parse(data.ResultSet);
                $('#len').html(json_data);
            });
            return json_data;
        };

        var stats = get_data();
        function update() {
            stats = get_data();
            console.log(stats);
        }
        setInterval(update, 1000);

        var canvas = document.getElementById("user-defined");
        canvas.style.backgroundColor = "rgba(255, 255, 255, 1)";
        var ctx = canvas.getContext('2d');
        ctx.canvas.height = 100;
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [
                    {%- for key, value in datasets.items() %}
                    {
                        {{ key }}
                        label: "{{ value.label }}",
                        data: [],
                        borderColor: color(chartColors.red).alpha(0.8).rgbString(),
                        backgroundColor: chartColors.{{ value.color }},
                        pointBackgroundColor: "white",
                        pointBorderColor: "white",
                        fill: false
                    },
                    {% endfor %}
                ]
            },
            options: {
                scales: {
                    xAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: "{{ xaxes.label }}",
                                fontSize: {{ xaxes.fontSize }},
                                fontColor: "white"
                            },
                            ticks: {
                                fontSize: 18,
                                fontColor: "white"
                            },
                            type: 'realtime',
                            gridLines: {
                                color: "rgba(255, 255, 255, 0.5)",
                                lineWidth: 0.75
                            }
                        }
                    ],
                    yAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: "{{ yaxes.label }}",
                                fontSize: {{ yaxes.fontSize }},
                                fontColor: "white",
                            },
                            ticks: {
                                {%- raw %}
                                min: {{ graph.chart.user-defined.yaxes.min }},
                                max: {{ graph.chart.user-defined.yaxes.max }},
                                {%- endraw %}
                                fontSize: {{ ticks.fontSize }},
                                {%- raw %}
                                stepSize: {{ graph.chart.user-defined.yaxes.step }},
                                fontColor: "white",
                                showLabelBackdrop: false
                                {%- endraw %}
                            },
                            gridLines: {
                                color: "rgba(255, 255, 255, 0.5)",
                                lineWidth: 0.75
                            },
                            pointLabels: {
                                fontColor: 'white'
                            }
                        }
                    ],
                },
                layout: {
                    padding: {
                        left: 10,
                        right: 10,
                        top: 10,
                        bottom: 10
                    }
                },
                legend: {
                    position: 'top',
                    labels: {
                        fontColor: 'white',
                        fontSize: 18,
                    },
                },
                plugins: {
                    streaming: {
                        {%- raw %}
                        duration: {{ graph.chart.user-defined.streaming.duration }},
                        {%- endraw %}
                        refresh: 1000,
                        delay: 1000,
                        frameRate: 30,
                        pause: false,
                        onRefresh: function(chart) {
                            chart.data.datasets[0].data.push({
                                x: Date.now(),
                                y: stats.data
                            });
                        }
                    },
                }
            }
        });

      Chart.plugins.register({
        beforeDraw: function(chartInstance) {
          var ctx = chartInstance.chart.ctx;
          ctx.fillStyle = "rgba(50, 50, 50, 1)";
          ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
        }
      })
    </script>
    """
    t = Template(s)
    with open("test.json") as f:
        data = json.load(f)
    print(t.render(data))
    print(type(t.render(data)))
    return s


make_script()



def make_body():
    script = make_script()
    html = """
    <div class="column is-8">
            <section>
            <div class="container">
                <div class="content">
                    <h1 class="title">
                        CPU user-defined
                    </h1>
                    <canvas id="user-defined"></canvas>
                </div>
            </div>
        </section>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.3.0/chart.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment-with-locales.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-streaming@latest/dist/chartjs-plugin-streaming.min.js"></script>
    {:}
    """.format(script)
    return html


tmp = """
{%- raw %}
{% extends "layout.html" %}
{% block content %}
{%- endraw %}
{{ body }}
{%- raw %}
{% endblock %}
{%- endraw %}
"""

#t = Template(tmp)
#data = {"body": "a"}
#print(t.render(data))


#print(make_body())
#t2 = Template(make_body())
#graph = {"graph": "a"}
#print(t2.render(graph))
