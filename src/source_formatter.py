def format_sources(docs):

    sources = []

    seen = set()

    for doc in docs:

        source = doc.metadata.get("source")


        if source in seen:
            continue


        seen.add(source)


        if source.startswith("http"):

            sources.append(
                f"🌐 Website: {source}"
            )

        else:

            page = doc.metadata.get("page")

            sources.append(
                f"📄 Document: {source} | Page: {page + 1}"
            )


    return sources