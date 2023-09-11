from __future__ import annotations
# [START tutorial]
# [START import_module]
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

# [START instantiate_dag]
with DAG(
    "test_dag",
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    # [END default_args]
    description="Mike's ETL test DAG",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["crwaling"],
) as dag:
    t1 = BashOperator(
        task_id="crawl_naverDocIds",
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh naverDocid",
    )

    t2 = BashOperator(
        task_id="crawl_70101",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh crawlQuestion 70101",
        retries=3,
    )
    
    t3 = BashOperator(
        task_id="crawl_70102",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh crawlQuestion 70102",
        retries=3,
    )

    t4 = BashOperator(
        task_id="crawl_70106",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh crawlQuestion 70106",
        retries=3,
    )

    t5 = BashOperator(
        task_id="crawl_70111",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh crawlQuestion 70111",
        retries=3,
    )
    
    t6 = BashOperator(
        task_id="crawl_70112",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh crawlQuestion 70112",
        retries=3,
    )

    t7 = BashOperator(
        task_id="crawl_70113",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh crawlQuestion 70113",
        retries=3,
    )

    t8 = BashOperator(
        task_id="crawl_70114",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh crawlQuestion 70114",
        retries=3,
    )   
    
    t9 = BashOperator(
        task_id="Gather_all_Crawled_json_file",
        depends_on_past=False,
        bash_command="ssh hosapp ~/volume/bin/crawl_trigger.sh Gathering",
        retries=3,
    )
    
    # [START documentation]
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    # [END documentation]

    # [START jinja_template]
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    # [END jinja_template]

    # 
    t1 >> [t2, t3, t4, t5, t6, t7, t8] >> t9
    
    # test run
    # t1 >> [t2, t3, t7, t8]