#!/bin/bash

echo 'Dumping schema (without data) to sms-survey-dashboard.sql'
pg_dump -s sms-survey-dashboard > ../sql/sms-survey-dashboard.sql
