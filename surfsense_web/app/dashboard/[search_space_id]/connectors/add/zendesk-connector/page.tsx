"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { IconTicket } from "@tabler/icons-react";
import { motion } from "framer-motion";
import { useParams, useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
	Form,
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useCreateConnector } from "@/hooks/use-connectors";
import { SearchSourceConnectorType } from "@/lib/api";

const FormSchema = z.object({
	name: z.string().min(2, {
		message: "Name must be at least 2 characters.",
	}),
	zendeskSubdomain: z.string().min(1, {
		message: "Zendesk Subdomain is required.",
	}),
	zendeskEmail: z.string().email({
		message: "Invalid email address.",
	}),
	zendeskApiToken: z.string().min(1, {
		message: "Zendesk API Token is required.",
	}),
});

export default function AddZendeskConnectorPage() {
	const params = useParams();
	const router = useRouter();
	const searchSpaceId = params.search_space_id as string;

	const createConnector = useCreateConnector();

	const form = useForm<z.infer<typeof FormSchema>>({
		resolver: zodResolver(FormSchema),
		defaultValues: {
			name: "",
			zendeskSubdomain: "",
			zendeskEmail: "",
			zendeskApiToken: "",
		},
	});

	async function onSubmit(data: z.infer<typeof FormSchema>) {
		try {
			await createConnector.mutateAsync({
				name: data.name,
				connector_type: SearchSourceConnectorType.ZENDESK_CONNECTOR,
				is_indexable: true,
				config: {
					ZENDESK_SUBDOMAIN: data.zendeskSubdomain,
					ZENDESK_EMAIL: data.zendeskEmail,
					ZENDESK_API_TOKEN: data.zendeskApiToken,
				},
			});

			toast.success("Zendesk connector created successfully!");
			router.push(`/dashboard/${searchSpaceId}/connectors`);
		} catch (error: any) {
			toast.error(error.message || "Failed to create Zendesk connector.");
		}
	}

	return (
		<div className="container mx-auto py-12 max-w-3xl">
			<motion.div
				initial={{ opacity: 0, y: 30 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{
					duration: 0.6,
					ease: [0.22, 1, 0.36, 1],
				}}
				className="mb-8 text-center"
			>
				<div className="flex items-center justify-center mb-4">
					<div className="flex h-20 w-20 items-center justify-center rounded-full bg-primary/10 dark:bg-primary/20">
						<IconTicket className="h-10 w-10 text-primary" />
					</div>
				</div>
				<h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-purple-500 to-indigo-500 bg-clip-text text-transparent">
					Add Zendesk Connector
				</h1>
				<p className="text-muted-foreground mt-3 text-lg max-w-2xl mx-auto">
					Connect your Zendesk account to index and search tickets and help center articles.
				</p>
			</motion.div>

			<Card className="w-full">
				<CardHeader>
					<CardTitle>Zendesk Configuration</CardTitle>
				</CardHeader>
				<CardContent>
					<Form {...form}>
						<form onSubmit={form.handleSubmit(onSubmit)} className="w-full space-y-6">
							<FormField
								control={form.control}
								name="name"
								render={({ field }) => (
									<FormItem>
										<FormLabel>Connector Name</FormLabel>
										<FormControl>
											<Input placeholder="My Zendesk" {...field} />
										</FormControl>
										<FormDescription>A friendly name for your Zendesk connector.</FormDescription>
										<FormMessage />
									</FormItem>
								)}
							/>
							<FormField
								control={form.control}
								name="zendeskSubdomain"
								render={({ field }) => (
									<FormItem>
										<FormLabel>Zendesk Subdomain</FormLabel>
										<FormControl>
											<Input placeholder="yourcompany" {...field} />
										</FormControl>
										<FormDescription>
											Your Zendesk subdomain (e.g., "yourcompany" for yourcompany.zendesk.com).
										</FormDescription>
										<FormMessage />
									</FormItem>
								)}
							/>
							<FormField
								control={form.control}
								name="zendeskEmail"
								render={({ field }) => (
									<FormItem>
										<FormLabel>Zendesk Email</FormLabel>
										<FormControl>
											<Input placeholder="admin@example.com" {...field} />
										</FormControl>
										<FormDescription>
											The email address of an admin user for authentication.
										</FormDescription>
										<FormMessage />
									</FormItem>
								)}
							/>
							<FormField
								control={form.control}
								name="zendeskApiToken"
								render={({ field }) => (
									<FormItem>
										<FormLabel>Zendesk API Token</FormLabel>
										<FormControl>
											<Input type="password" placeholder="zd_..." {...field} />
										</FormControl>
										<FormDescription>
											Your Zendesk API token. You can generate one in your Zendesk Admin Center.
										</FormDescription>
										<FormMessage />
									</FormItem>
								)}
							/>
							<Button type="submit" className="w-full" disabled={createConnector.isPending}>
								{createConnector.isPending ? "Adding Connector..." : "Add Zendesk Connector"}
							</Button>
						</form>
					</Form>
				</CardContent>
			</Card>
		</div>
	);
}
