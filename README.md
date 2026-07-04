SQL Server Heirarchy:
	Database:
		Schemas:
			- Project
				Tables:
					- advisor_documents: which advisor gets what information
						cols: advisor_id, document_id, weight, relevance_note 


					- advisors: basic info on advisors
						cols: advisor_id, name, description, config


					- chunks: chunks of text from documents
						cols: chunk_id, document_id, chunk_index, chunk_text, token_count, embedding, embedding model
						

					- documents: catalogue of the documents
						cols: document_id, url, source_type, content_hash