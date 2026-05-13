# Official tech documentation roadmap (Mutter)

**Purpose:** Central list of **official documentation** links for common programming languages, databases, frameworks, DevOps tools, and ML stacks.

**Agent workflow (token-efficient):**

1. When you need language/API/framework/database docs or a trustworthy spec URL, **check this file first** (use workspace search or read **only** the section heading you need, e.g. `## PostgreSQL` or `## FastAPI`). Prefer a link from here over unconstrained web search.
2. If the stack is **not** listed here, fall back to the lookup priority in [Notes For AI Plugins](#notes-for-ai-plugins) at the bottom of this file.
3. **Never** paste this entire file into chat; open the file in the editor and pull **one** subsection.

**Maintenance:** Extend this roadmap with project-specific stacks (add a `## YourStack` block with official URLs). Keep entries link-forward; avoid long prose.

---

# Programming Languages, Official Documentation, Databases, and Frameworks Reference Guide

This document is designed as a centralized knowledge base for AI tooling, agents, plugins, and assistants to quickly locate official documentation, API references, specifications, guides, and framework ecosystems.

---

# 1. Most Popular Programming Languages

## 1. Python

- Official Website:
  - https://www.python.org/
- Official Documentation:
  - https://docs.python.org/3/
- Package Repository:
  - https://pypi.org/
- Language Reference:
  - https://docs.python.org/3/reference/
- Standard Library:
  - https://docs.python.org/3/library/
- Typing:
  - https://docs.python.org/3/library/typing.html
- AsyncIO:
  - https://docs.python.org/3/library/asyncio.html
- Virtual Environments:
  - https://docs.python.org/3/library/venv.html
- Packaging:
  - https://packaging.python.org/
- PEP Index:
  - https://peps.python.org/

Specifics:
- Huge ecosystem
- AI/ML dominance
- Excellent documentation structure
- Official typing system
- Massive standard library

---

## 2. JavaScript

- Official Documentation:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript
- ECMAScript Specification:
  - https://tc39.es/ecma262/
- Node.js:
  - https://nodejs.org/en/docs
- NPM:
  - https://docs.npmjs.com/

Specifics:
- Browser-native language
- Event-driven architecture
- Async by default
- Largest frontend ecosystem

---

## 3. TypeScript

- Official Documentation:
  - https://www.typescriptlang.org/docs/
- Handbook:
  - https://www.typescriptlang.org/docs/handbook/intro.html
- TSConfig:
  - https://www.typescriptlang.org/tsconfig

Specifics:
- Static typing over JavaScript
- Enterprise-scale frontend/backend
- Excellent IDE tooling

---

## 4. Java

- Official Documentation:
  - https://docs.oracle.com/en/java/
- OpenJDK:
  - https://openjdk.org/
- JVM Specs:
  - https://docs.oracle.com/javase/specs/

Specifics:
- Enterprise systems
- JVM ecosystem
- Strong backward compatibility

---

## 5. C#

- Official Documentation:
  - https://learn.microsoft.com/en-us/dotnet/csharp/
- .NET Docs:
  - https://learn.microsoft.com/en-us/dotnet/

Specifics:
- Microsoft ecosystem
- Excellent tooling
- Cross-platform with .NET

---

## 6. PHP

- Official Documentation:
  - https://www.php.net/docs.php
- Language Reference:
  - https://www.php.net/manual/en/langref.php
- Composer:
  - https://getcomposer.org/doc/

Specifics:
- Web-focused
- Huge CMS ecosystem
- Shared hosting compatibility

---

## 7. Go (Golang)

- Official Documentation:
  - https://go.dev/doc/
- Packages:
  - https://pkg.go.dev/
- Language Spec:
  - https://go.dev/ref/spec

Specifics:
- Concurrency-first
- Lightweight binaries
- Cloud-native tooling

---

## 8. Rust

- Official Documentation:
  - https://www.rust-lang.org/learn
- Rust Book:
  - https://doc.rust-lang.org/book/
- Cargo:
  - https://doc.rust-lang.org/cargo/
- Crates:
  - https://crates.io/

Specifics:
- Memory safety
- Ownership model
- Systems programming

---

## 9. C

- Official Reference:
  - https://en.cppreference.com/w/c
- GCC:
  - https://gcc.gnu.org/onlinedocs/

Specifics:
- Low-level systems language
- OS/kernel development

---

## 10. C++

- Official Reference:
  - https://en.cppreference.com/w/cpp
- ISO C++:
  - https://isocpp.org/

Specifics:
- High performance
- STL
- Game engines and systems

---

## 11. Kotlin

- Official Documentation:
  - https://kotlinlang.org/docs/home.html

Specifics:
- Android-first
- JVM compatible
- Concise syntax

---

## 12. Swift

- Official Documentation:
  - https://developer.apple.com/swift/
- Swift Book:
  - https://docs.swift.org/swift-book/

Specifics:
- Apple ecosystem
- iOS/macOS apps

---

## 13. Ruby

- Official Documentation:
  - https://www.ruby-lang.org/en/documentation/
- Ruby API:
  - https://ruby-doc.org/

Specifics:
- Developer productivity
- Convention over configuration

---

## 14. Dart

- Official Documentation:
  - https://dart.dev/guides
- API:
  - https://api.dart.dev/

Specifics:
- Flutter ecosystem
- Cross-platform apps

---

## 15. R

- Official Documentation:
  - https://cran.r-project.org/manuals.html

Specifics:
- Statistical computing
- Data science

---

## 16. MATLAB

- Documentation:
  - https://www.mathworks.com/help/

Specifics:
- Scientific computing
- Engineering simulations

---

## 17. Scala

- Official Documentation:
  - https://docs.scala-lang.org/

Specifics:
- Functional + OOP
- JVM ecosystem

---

## 18. Perl

- Official Documentation:
  - https://perldoc.perl.org/

Specifics:
- Text processing
- Scripting

---

## 19. Lua

- Official Documentation:
  - https://www.lua.org/docs.html

Specifics:
- Embedded scripting
- Game development

---

## 20. Haskell

- Official Documentation:
  - https://www.haskell.org/documentation/

Specifics:
- Pure functional language

---

## 21. Elixir

- Official Documentation:
  - https://elixir-lang.org/docs.html

Specifics:
- Erlang VM
- Massive concurrency

---

## 22. Erlang

- Official Documentation:
  - https://www.erlang.org/docs

Specifics:
- Telecom systems
- Fault tolerance

---

## 23. Objective-C

- Apple Documentation:
  - https://developer.apple.com/documentation/objectivec

Specifics:
- Legacy Apple ecosystem

---

## 24. Shell/Bash

- GNU Bash:
  - https://www.gnu.org/software/bash/manual/

Specifics:
- Linux automation
- DevOps scripting

---

## 25. PowerShell

- Official Documentation:
  - https://learn.microsoft.com/en-us/powershell/

Specifics:
- Windows automation

---

## 26. Julia

- Official Documentation:
  - https://docs.julialang.org/

Specifics:
- Scientific computing
- High-performance math

---

## 27. Assembly

- NASM:
  - https://www.nasm.us/doc/

Specifics:
- CPU-level programming

---

## 28. COBOL

- Documentation:
  - https://www.ibm.com/docs/en/cobol-zos

Specifics:
- Banking systems

---

## 29. Fortran

- Documentation:
  - https://fortran-lang.org/learn/

Specifics:
- Scientific computing

---

## 30. SQL

- PostgreSQL SQL Docs:
  - https://www.postgresql.org/docs/current/sql.html
- MySQL SQL:
  - https://dev.mysql.com/doc/

Specifics:
- Database querying
- Relational systems

---

# 2. Most Popular Databases

## PostgreSQL

- Official Docs:
  - https://www.postgresql.org/docs/
- SQL Commands:
  - https://www.postgresql.org/docs/current/sql-commands.html
- Extensions:
  - https://www.postgresql.org/docs/current/external-extensions.html
- JSON:
  - https://www.postgresql.org/docs/current/functions-json.html
- Performance:
  - https://www.postgresql.org/docs/current/performance-tips.html

Specifics:
- ACID compliant
- Advanced SQL support
- JSONB support
- Extensions ecosystem

---

## MySQL

- Official Docs:
  - https://dev.mysql.com/doc/
- Reference Manual:
  - https://dev.mysql.com/doc/refman/8.0/en/

Specifics:
- Popular web database
- Replication support

---

## MariaDB

- Official Docs:
  - https://mariadb.com/kb/en/documentation/

Specifics:
- MySQL fork
- Open-source focused

---

## MongoDB

- Official Docs:
  - https://www.mongodb.com/docs/
- Aggregation:
  - https://www.mongodb.com/docs/manual/aggregation/

Specifics:
- NoSQL document DB
- BSON documents

---

## Redis

- Official Docs:
  - https://redis.io/docs/

Specifics:
- In-memory database
- Cache and queue support

---

## SQLite

- Official Docs:
  - https://www.sqlite.org/docs.html

Specifics:
- Embedded DB
- Zero configuration

---

## Elasticsearch

- Official Docs:
  - https://www.elastic.co/guide/index.html

Specifics:
- Full-text search
- Distributed indexing

---

## Cassandra

- Official Docs:
  - https://cassandra.apache.org/doc/latest/

Specifics:
- Distributed NoSQL
- High availability

---

## Oracle Database

- Official Docs:
  - https://docs.oracle.com/en/database/

Specifics:
- Enterprise-grade database

---

## Microsoft SQL Server

- Official Docs:
  - https://learn.microsoft.com/en-us/sql/sql-server/

Specifics:
- Microsoft ecosystem
- Enterprise analytics

---

## Neo4j

- Official Docs:
  - https://neo4j.com/docs/

Specifics:
- Graph database

---

## CouchDB

- Official Docs:
  - https://docs.couchdb.org/

Specifics:
- Document-based
- Sync support

---

## DynamoDB

- Official Docs:
  - https://docs.aws.amazon.com/dynamodb/

Specifics:
- AWS managed NoSQL

---

## Firestore

- Official Docs:
  - https://firebase.google.com/docs/firestore

Specifics:
- Firebase ecosystem
- Realtime synchronization

---

## InfluxDB

- Official Docs:
  - https://docs.influxdata.com/

Specifics:
- Time-series database

---

# 3. Most Popular Frameworks By Language

# Python Frameworks

## Django

- Docs:
  - https://docs.djangoproject.com/
- ORM:
  - https://docs.djangoproject.com/en/stable/topics/db/
- Authentication:
  - https://docs.djangoproject.com/en/stable/topics/auth/
- REST:
  - https://www.django-rest-framework.org/

Specifics:
- Batteries included
- ORM
- Admin panel

---

## FastAPI

- Docs:
  - https://fastapi.tiangolo.com/
- Dependency Injection:
  - https://fastapi.tiangolo.com/tutorial/dependencies/
- Security:
  - https://fastapi.tiangolo.com/tutorial/security/

Specifics:
- Async-first
- OpenAPI support

---

## Flask

- Docs:
  - https://flask.palletsprojects.com/

Specifics:
- Minimal framework
- WSGI based

---

# PHP Frameworks

## Symfony

- Docs:
  - https://symfony.com/doc/current/index.html
- Components:
  - https://symfony.com/components
- Security:
  - https://symfony.com/doc/current/security.html
- Messenger:
  - https://symfony.com/doc/current/messenger.html

Specifics:
- Enterprise-grade
- Component-based architecture

---

## Laravel

- Docs:
  - https://laravel.com/docs
- Eloquent:
  - https://laravel.com/docs/eloquent
- Queues:
  - https://laravel.com/docs/queues
- Events:
  - https://laravel.com/docs/events

Specifics:
- Rapid development
- Huge ecosystem

---

# JavaScript / TypeScript Frameworks

## React

- Docs:
  - https://react.dev/
- Hooks:
  - https://react.dev/reference/react
- Router:
  - https://reactrouter.com/en/main

Specifics:
- Component architecture
- Virtual DOM

---

## Next.js

- Docs:
  - https://nextjs.org/docs
- App Router:
  - https://nextjs.org/docs/app
- Server Actions:
  - https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions

Specifics:
- SSR/SSG
- Full-stack React

---

## Vue.js

- Docs:
  - https://vuejs.org/guide/
- Composition API:
  - https://vuejs.org/guide/extras/composition-api-faq.html

Specifics:
- Easy learning curve

---

## Nuxt

- Docs:
  - https://nuxt.com/docs

Specifics:
- Full-stack Vue framework

---

## Angular

- Docs:
  - https://angular.dev/
- RxJS:
  - https://rxjs.dev/

Specifics:
- Enterprise frontend

---

## SvelteKit

- Docs:
  - https://kit.svelte.dev/docs/introduction

Specifics:
- Compile-time optimization

---

## NestJS

- Docs:
  - https://docs.nestjs.com/
- Microservices:
  - https://docs.nestjs.com/microservices/basics
- WebSockets:
  - https://docs.nestjs.com/websockets/gateways

Specifics:
- Enterprise Node.js backend

---

## Express.js

- Docs:
  - https://expressjs.com/

Specifics:
- Minimal Node.js framework

---

# Java Frameworks

## Spring Boot

- Docs:
  - https://docs.spring.io/spring-boot/docs/current/reference/html/
- Spring Security:
  - https://docs.spring.io/spring-security/reference/
- Spring Data:
  - https://spring.io/projects/spring-data

Specifics:
- Enterprise backend ecosystem

---

## Quarkus

- Docs:
  - https://quarkus.io/guides/

Specifics:
- Kubernetes-native Java

---

# C# Frameworks

## ASP.NET Core

- Docs:
  - https://learn.microsoft.com/en-us/aspnet/core/

Specifics:
- Cross-platform .NET web framework

---

# Go Frameworks

## Gin

- Docs:
  - https://gin-gonic.com/docs/

Specifics:
- Lightweight HTTP framework

---

## Fiber

- Docs:
  - https://docs.gofiber.io/

Specifics:
- Express-like Go framework

---

# Rust Frameworks

## Actix Web

- Docs:
  - https://actix.rs/docs/

Specifics:
- High-performance async framework

---

## Rocket

- Docs:
  - https://rocket.rs/guide/

Specifics:
- Type-safe web framework

---

# Ruby Frameworks

## Ruby on Rails

- Docs:
  - https://rubyonrails.org/docs

Specifics:
- Convention over configuration

---

# Kotlin Frameworks

## Ktor

- Docs:
  - https://ktor.io/docs/

Specifics:
- Kotlin-native backend

---

# Dart Frameworks

## Flutter

- Docs:
  - https://docs.flutter.dev/

Specifics:
- Cross-platform mobile apps

---

# DevOps / Infrastructure Related

## Docker

- Docs:
  - https://docs.docker.com/

---

## Kubernetes

- Docs:
  - https://kubernetes.io/docs/

---

## Terraform

- Docs:
  - https://developer.hashicorp.com/terraform/docs

---

## Ansible

- Docs:
  - https://docs.ansible.com/

---

# AI / Machine Learning Frameworks

## TensorFlow

- Docs:
  - https://www.tensorflow.org/learn

---

## PyTorch

- Docs:
  - https://pytorch.org/docs/stable/index.html

---

## Hugging Face Transformers

- Docs:
  - https://huggingface.co/docs/transformers/index

---

# Useful Universal Documentation Resources

## MDN Web Docs

- https://developer.mozilla.org/

Specifics:
- Best frontend/web reference

---

## Stack Overflow

- https://stackoverflow.com/

Specifics:
- Community solutions

---

## DevDocs

- https://devdocs.io/

Specifics:
- Unified offline documentation browser

---

## W3C

- https://www.w3.org/

Specifics:
- Web standards

---

## Agent harness — plugin authoring (Mutter repo)

- **OpenAI Codex — plugins overview:** https://developers.openai.com/codex/plugins
- **OpenAI Codex — build plugins (manifest, skills, marketplaces):** https://developers.openai.com/codex/plugins/build
- **OpenCode — plugins (JS/TS hooks, npm/git install):** https://opencode.ai/docs/plugins/

---

# Notes For AI Plugins

Recommended AI lookup priority:

1. Official documentation
2. Official GitHub repository
3. RFC/specification
4. Community-maintained docs
5. Stack Overflow discussions
6. Reddit discussions
7. Blog posts

Recommended indexing categories:

- language
- framework
- runtime
- package-manager
- ORM
- database
- cloud
- devops
- frontend
- backend
- mobile
- testing
- security
- deployment
- API
- websocket
- authentication
- caching
- queue
- containerization
