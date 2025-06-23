from loguru import logger
from llm_judge import Evaluator
from datetime import datetime
from pathlib import Path
import statistics
import time

from multi_agent_system.character_agent import CharacterAgent
from multi_agent_system.locations_agent import LocationsAgent
from multi_agent_system.town_agent import TownAgent
from multi_agent_system.world_agent import WorldAgent
from multi_agent_system.storyteller import Storyteller
from multi_agent_system.supervisor import Supervisor


def run(query):
    logger.info("Starting...")
    supervisor = Supervisor()
    supervisor.define_agent(WorldAgent)
    supervisor.define_agent(LocationsAgent)
    supervisor.define_agent(CharacterAgent)
    supervisor.define_agent(TownAgent)
    result = supervisor.handle_query(query)
    logger.info("Model Result:")
    logger.info(result)
    return result


def benchmark_queries(query_descriptions, repeat=1):
    evaluator = Evaluator()
    all_results = []

    for _ in range(repeat):
        for item in query_descriptions:
            if isinstance(item, tuple) and len(item) == 2:
                query, description = item
            else:
                query = item
                description = None

            start_time = time.time()
            result = run(query)
            elapsed = time.time() - start_time
            evaluation = evaluator.evaluate(query, result, description)
            all_results.append(
                {
                    "query": query,
                    "description": description,
                    "result": result,
                    "evaluation": evaluation,
                    "timestamp": datetime.now().isoformat(),
                    "execution_time": elapsed,
                }
            )

    return all_results


def save_results(results, output_dir="benchmarks"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"benchmark_{timestamp}.md"

    # Calculate median scores per metric
    metrics = {}
    for result in results:
        for metric, eval_data in result["evaluation"].items():
            if metric not in metrics:
                metrics[metric] = []
            metrics[metric].append(eval_data["score"])

    median_scores = {
        metric: statistics.median(scores) for metric, scores in metrics.items()
    }

    execution_times = [r["execution_time"] for r in results]
    median_time = statistics.median(execution_times)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Model Benchmark Results\n\n")
        f.write(f"Generated at: {timestamp}\n\n")
        f.write("## Summary Statistics\n")
        f.write(f"- **Median Execution Time**: {median_time:.2f} seconds\n")

        for metric, median in median_scores.items():
            if metric == "rouge_l":
                f.write(f"- **Median ROUGE-L**: {median:.4f}\n")
            else:
                f.write(f"- **Median {metric.capitalize()}**: {median:.1f}/100\n")

        f.write("\n## Detailed Results\n\n")

        for i, result in enumerate(results, 1):
            f.write(f"### Evaluation {i}\n")
            f.write(f"**Query:** {result['query']}\n\n")
            f.write(f"**Result:** {result['result']}\n\n")
            f.write("**Scores:**\n")

            for metric, eval_data in result["evaluation"].items():
                if metric == "rouge_l":
                    f.write(f"- ROUGE-L: {eval_data['score']:.4f}\n")
                else:
                    f.write(f"- {metric.capitalize()}: {eval_data['score']}/100\n")

            f.write(f"\n**Timestamp**: {result['timestamp']}\n")
            f.write(f"**Execution Time**: {result['execution_time']:.2f} seconds\n\n")

    return str(output_path)


if __name__ == "__main__":
    logger.disable(None)

    query_descriptions = [
        (
            "Создайте описание приключения, в котором герои отправляются в зачарованный лес, чтобы найти потерянный артефакт.",
            "Вы стоите у входа в зачарованный лес, известный как Лес Тысячи Шепотов. Деревья здесь высокие и густые, их ветви переплетаются, образуя почти непроницаемый купол. Солнечный свет едва проникает сквозь листву, создавая игру света и тени на земле, а в воздухе витает запах мха и влажной земли. Где-то вдалеке слышен шорох листьев и тихий шепот, который, как говорят, исходит от духов леса. Ваша цель — найти потерянный артефакт, Кристалл Вечной Жизни, спрятанный, по легенде, в самом сердце леса. Путь обещает быть опасным, ведь лес охраняют древние стражи.",
        ),
        (
            "Опишите сцену, в которой герои готовятся спасти похищенную принцессу из тёмного замка.",
            "Вы стоите у подножия мрачного замка, возвышающегося на вершине скалы. Стены покрыты мхом и лишайником, окна забраны ржавыми решётками, а над воротами висит зловещий герб с изображением чёрного дракона. Ветер воет, проносясь через развалины, и доносится далёкий крик совы. Ваша миссия — спасти похищенную принцессу, заточённую в темнице под замком. Говорят, что её стережёт не только стража, но и тёмные силы, пробуждённые хозяином этого места.",
        ),
        (
            "Создайте описание приключения, в котором герои расследуют серию таинственных исчезновений в оживлённом городе.",
            "Вы находитесь в центре оживлённого города, известного как Город Тысячи Огней. Узкие извилистые улицы заполнены шумом толпы, а высокие дома теснятся друг к другу. В воздухе витает запах специй и дыма от лавок и мастерских, а фонари отбрасывают длинные тени на мостовую. В последнее время город охвачен страхом: люди исчезают без следа, оставляя за собой лишь слухи о тёмной фигуре, мелькающей в ночи. Ваша задача — раскрыть тайну и найти пропавших, пока не стало слишком поздно.",
        ),
        (
            "Опишите сцену, в которой герои отправляются в путешествие через раскалённую пустыню, чтобы найти скрытый оазис.",
            "Вы стоите на краю бескрайней Пустыни Вечного Песка. Песок под ногами раскалён, словно угли, а вдалеке виднеются дюны, подобные горам. Ветер несёт песок, забивающийся в глаза и одежду, и солнце палит нещадно, превращая воздух в дрожащее марево. Ваша цель — найти скрытый оазис, о котором ходят легенды: говорят, его воды обладают магической силой исцеления. Но путь через пустыню сулит испытания — миражи, жара и хищники подстерегают вас.",
        ),
        (
            "Создайте описание приключения, в котором герои погружаются под воду, чтобы исследовать затонувший корабль.",
            "Вы стоите на борту небольшого судна, качающегося на волнах над местом, где затонул старинный корабль. Вода под вами глубокая и тёмная, словно бездонная пропасть, и лишь слабые отблески света проникают в её глубины. Погрузившись, вы видите очертания корабля, покрытого водорослями и кораллами. Говорят, он хранит сокровища и тайны давно забытой эпохи, но под водой вас могут ждать опасности — от острых обломков до морских тварей, охраняющих свои владения.",
        ),
        (
            "Опишите сцену, в которой герои готовятся сразиться с могущественным колдуном, захватившим королевство.",
            "Вы стоите у ворот королевского замка, теперь окутанного тёмной магией. Небо затянуто чёрными тучами, молнии освещают мрачные башни, а в воздухе пахнет озоном и гарью. Могучий колдун, захвативший королевство, ждёт в тронном зале, окружённый своими прислужниками. Его сила ощущается даже здесь — земля дрожит от заклинаний. Вам предстоит бросить вызов этой тьме, чтобы вернуть свободу землям, но победа потребует не только смелости, но и хитрости.",
        ),
        (
            "Создайте описание приключения, в котором герои пересекают заснеженный горный перевал, чтобы доставить важное сообщение.",
            "Вы стоите у подножия заснеженного горного перевала, где ветер завывает, неся снежные вихри. Снег покрывает всё вокруг толстым слоем, и видимость почти нулевая, лишь смутные очертания скал проступают сквозь метель. Ваша задача — доставить важное сообщение в деревню по ту сторону гор, но путь опасен: лавины гремят в вышине, а ледяные трещины скрыты под снегом. Где-то в отдалении слышен вой волков, напоминающий о том, что вы не одни в этой пустыне льда.",
        ),
        (
            "Опишите сцену, в которой герои исследуют древний заброшенный храм в поисках скрытых знаний.",
            "Вы стоите перед входом в древний храм, заброшенный века назад. Стены покрыты мхом и лианами, а вход завален обломками камней. Внутри царит тьма, нарушаемая лишь эхом ваших шагов и слабым светом, пробивающимся через трещины в потолке. Воздух пропитан сыростью и запахом старости. Легенды гласят, что здесь спрятаны тайные знания древних, но храм полон ловушек и загадок, охраняющих свои секреты от незваных гостей.",
        ),
        (
            "Создайте описание приключения, в котором герои проникают в хорошо охраняемую крепость, чтобы украсть ценный артефакт.",
            "Вы притаились у стен крепости, окружённой высокими башнями и охраняемой множеством стражников. Толстые каменные стены кажутся неприступными, а ворота заперты на тяжёлые засовы. Свет факелов отражается от доспехов патрулей, чьи шаги разносятся в ночной тишине. Ваша цель — проникнуть внутрь и выкрасть ценный артефакт из сокровищницы, но одно неверное движение может поднять тревогу. Тени — ваши союзники в этой миссии, где всё зависит от stealth и смекалки.",
        ),
        (
            "Опишите сцену, в которой герои оказываются на необитаемом острове и должны найти способ выбраться.",
            "Вы стоите на берегу необитаемого острова, окружённого бескрайним океаном. Волны бьют о скалы, а над головой кричат чайки. Позади вас — густые джунгли, полные шорохов и скрытых опасностей, от ядовитых змей до диких зверей. Корабль, на котором вы плыли, разбит штормом, и теперь ваша задача — найти способ выбраться: построить плот или подать сигнал о помощи. Ресурсов мало, а время работает против вас в этом суровом испытании выживания.",
        ),
    ]

    results = benchmark_queries(query_descriptions, repeat=1)
    output_path = save_results(results)
    logger.info(f"Saved benchmark results to: {output_path}")
