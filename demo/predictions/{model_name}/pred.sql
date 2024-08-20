select company.headquarters from company where  company.industry = "Banking"   intersect select company.headquarters from company where  company.industry = "Oil and gas"
