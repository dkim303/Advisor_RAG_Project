SQL Server Heirarchy:
	Database:
		Schemas:
			- Public
				Tables:
					- advisor_documents: which advisor gets what information
						cols: advisor_id, document_id, weight, relevance_note 

					- advisors: basic info on advisors
						cols: advisor_id, name, description, config

					- chunks: chunks of text from documents
						cols: chunk_id, document_id, chunk_index, chunk_text, token_count
						
					- documents: catalogue of the documents
						cols: document_id, title, source_name, source_type, url, author, published_at, ingested_at, cleaned_text, content_hash