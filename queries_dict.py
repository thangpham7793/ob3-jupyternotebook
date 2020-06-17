from cloud import session

admin_queries = {
  'logins_over_time': session.prepare('''
  SELECT status, association, CAST(login_time AS text) as date, user_id, new_user
  FROM user_by_activity 
  WHERE month = ?;'''),
  
  'file_usage_by_course': session.prepare('''
  SELECT course_id, paper_id, type, sum(cast(size AS DOUBLE))/1000 as size_in_mb from file_usage_by_month 
  WHERE month = ?
  AND association = ?
  GROUP BY course_id, paper_id, type;
  '''),

  'data_usage_by_month': session.prepare('''
  SELECT association, course_id, paper_id, type, SUM(CAST(size AS DOUBLE))/1000 AS size_in_mb 
  FROM file_usage_by_month 
  WHERE month = ?
  AND association IN ('uniA', 'uniB', 'uniC')
  GROUP BY association, course_id, paper_id, type;
  '''),

  'contributions_by_course_or_paper': session.prepare('''
  SELECT paper_id, document_id, author_full_name, type, COUNT(type) as count
  FROM component
  WHERE course_id = ?
  AND paper_id = ?
  GROUP BY document_id, type;
  ''')
}

student_queries = {'foo' : 'bar'}

teacher_queries = {'foo' : 'baz'}
